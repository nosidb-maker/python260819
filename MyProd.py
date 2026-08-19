import sqlite3
from typing import Optional


class ProductDatabase:
    """Products 테이블의 생성과 CRUD 작업을 담당하는 클래스."""

    DB_PATH = r"c:\work\MyProduct.db"
    SAMPLE_COUNT = 100_000

    def __init__(self, db_path: str = DB_PATH) -> None:
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path, timeout=30)
        self.connection.execute("PRAGMA busy_timeout = 30000")
        self.create_table()

    @staticmethod
    def _validate_product(product_id: int, product_name: str, product_price: int) -> None:
        """제품 입력값을 검증한다."""
        if isinstance(product_id, bool) or not isinstance(product_id, int) or product_id <= 0:
            raise ValueError("product_id는 1 이상의 정수여야 합니다.")
        if not isinstance(product_name, str) or not product_name.strip():
            raise ValueError("product_name은 비어 있지 않은 문자열이어야 합니다.")
        if isinstance(product_price, bool) or not isinstance(product_price, int) or product_price < 0:
            raise ValueError("product_price는 0 이상의 정수여야 합니다.")

    def create_table(self) -> None:
        """Products 테이블이 없으면 생성한다."""
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS Products (
                    productID INTEGER PRIMARY KEY,
                    productName TEXT NOT NULL,
                    productPrice INTEGER NOT NULL,
                    CHECK (productID > 0),
                    CHECK (productPrice >= 0)
                )
                """
            )

    def insert_product(self, product_id: int, product_name: str, product_price: int) -> None:
        """제품 한 건을 입력한다."""
        self._validate_product(product_id, product_name, product_price)
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO Products (productID, productName, productPrice)
                VALUES (?, ?, ?)
                """,
                (product_id, product_name.strip(), product_price),
            )

    def update_product(self, product_id: int, product_name: str, product_price: int) -> int:
        """제품 한 건을 수정하고 수정된 행 수를 반환한다."""
        self._validate_product(product_id, product_name, product_price)
        with self.connection:
            cursor = self.connection.execute(
                """
                UPDATE Products
                SET productName = ?, productPrice = ?
                WHERE productID = ?
                """,
                (product_name.strip(), product_price, product_id),
            )
        return cursor.rowcount

    def delete_product(self, product_id: int) -> int:
        """제품 한 건을 삭제하고 삭제된 행 수를 반환한다."""
        if isinstance(product_id, bool) or not isinstance(product_id, int) or product_id <= 0:
            raise ValueError("product_id는 1 이상의 정수여야 합니다.")
        with self.connection:
            cursor = self.connection.execute(
                "DELETE FROM Products WHERE productID = ?",
                (product_id,),
            )
        return cursor.rowcount

    def select_products(
        self,
        product_id: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[tuple[int, str, int]]:
        """제품을 조회한다. product_id가 없으면 전체 또는 limit만큼 조회한다."""
        if product_id is not None:
            cursor = self.connection.execute(
                """
                SELECT productID, productName, productPrice
                FROM Products
                WHERE productID = ?
                """,
                (product_id,),
            )
        elif limit is not None:
            if limit < 0:
                raise ValueError("limit은 0 이상이어야 합니다.")
            cursor = self.connection.execute(
                """
                SELECT productID, productName, productPrice
                FROM Products
                ORDER BY productID
                LIMIT ?
                """,
                (limit,),
            )
        else:
            cursor = self.connection.execute(
                """
                SELECT productID, productName, productPrice
                FROM Products
                ORDER BY productID
                """
            )
        return cursor.fetchall()

    def seed_sample_data(self, count: int = SAMPLE_COUNT) -> int:
        """현재 데이터 수가 count보다 적을 때 샘플 데이터를 채운다."""
        if count < 0:
            raise ValueError("count는 0 이상이어야 합니다.")

        existing_ids = {
            row[0]
            for row in self.connection.execute(
                "SELECT productID FROM Products WHERE productID BETWEEN 1 AND ?",
                (count,),
            )
        }
        if len(existing_ids) == count:
            return 0

        rows = (
            (product_id, f"전자제품-{product_id:06d}", 10_000 + (product_id % 100) * 1_000)
            for product_id in range(1, count + 1)
            if product_id not in existing_ids
        )
        with self.connection:
            cursor = self.connection.executemany(
                """
                INSERT INTO Products (productID, productName, productPrice)
                VALUES (?, ?, ?)
                """,
                rows,
            )
        return cursor.rowcount

    def close(self) -> None:
        """데이터베이스 연결을 닫는다."""
        self.connection.close()


if __name__ == "__main__":
    database = ProductDatabase()
    try:
        inserted_count = database.seed_sample_data()
        print(f"샘플 데이터 {inserted_count:,}건을 준비했습니다.")
        print("조회 샘플:", database.select_products(limit=5))
    finally:
        database.close()