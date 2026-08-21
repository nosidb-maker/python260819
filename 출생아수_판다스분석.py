from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_FILE = Path("출생아수__합계출산율__자연증가_등_20240726084835.xlsx")
OUTPUT_DIR = Path("출생아수_분석결과")


def clean_data(input_file: Path) -> pd.DataFrame:
    """KOSIS 가로형 원본을 분석하기 좋은 세로형 데이터로 정리한다."""
    raw = pd.read_excel(input_file, sheet_name="데이터", header=None)

    year_values = raw.iloc[0, 1:]
    years = pd.to_numeric(
        year_values.astype(str).str.extract(r"(\d{4})", expand=False),
        errors="coerce",
    )

    cleaned = raw.iloc[1:, :].copy()
    cleaned.columns = ["항목"] + years.tolist()
    cleaned = cleaned.dropna(axis=1, how="all")
    cleaned = cleaned.set_index("항목")
    cleaned.index = cleaned.index.astype(str).str.strip()
    cleaned = cleaned.apply(pd.to_numeric, errors="coerce")

    result = cleaned.T.reset_index(names="연도")
    result["연도"] = pd.to_numeric(result["연도"], errors="coerce").astype("Int64")
    result = result.dropna(subset=["연도"]).sort_values("연도").reset_index(drop=True)
    result = result.drop_duplicates(subset=["연도"])
    return result


def save_birth_plot(data: pd.DataFrame, output_file: Path) -> None:
    plt.rcParams["font.family"] = ["Malgun Gothic", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    figure, axis = plt.subplots(figsize=(12, 6.5))
    axis.plot(
        data["연도"],
        data["출생아수(명)"],
        color="#0b7285",
        marker="o",
        markersize=3.5,
        linewidth=2,
    )
    axis.set_title("대한민국 연도별 출생아 수 (1970~2023)", fontsize=16, pad=14)
    axis.set_xlabel("연도")
    axis.set_ylabel("출생아 수(명)")
    axis.grid(axis="y", alpha=0.3)
    axis.spines[["top", "right"]].set_visible(False)
    axis.yaxis.set_major_formatter(lambda value, _: f"{value:,.0f}")
    figure.tight_layout()
    figure.savefig(output_file, dpi=160)
    plt.close(figure)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    data = clean_data(INPUT_FILE)

    numeric_columns = data.select_dtypes(include="number").columns
    missing = data.isna().sum()
    duplicate_years = int(data["연도"].duplicated().sum())

    data.to_csv(OUTPUT_DIR / "출생아수_정제데이터.csv", index=False, encoding="utf-8-sig")
    save_birth_plot(data, OUTPUT_DIR / "연도별_출생아수_라인그래프.png")

    summary = data[["출생아수(명)", "합계출산율(명)", "자연증가건수(명)"]].describe().T
    summary["변동폭"] = summary["max"] - summary["min"]
    summary.to_csv(OUTPUT_DIR / "기술통계.csv", encoding="utf-8-sig")

    recent = data.tail(10).set_index("연도")
    correlation = data[numeric_columns].corr()[["출생아수(명)", "합계출산율(명)"]]
    decade_change = data.set_index("연도")[["출생아수(명)", "합계출산율(명)"]].pct_change(10).tail(1)
    lowest_birth_year = data.loc[data["출생아수(명)"].idxmin(), ["연도", "출생아수(명)"]]
    highest_birth_year = data.loc[data["출생아수(명)"].idxmax(), ["연도", "출생아수(명)"]]

    data["출생아수_전년대비변화율"] = data["출생아수(명)"].pct_change()
    data["출생아수_감소여부"] = data["출생아수_전년대비변화율"] < 0
    data["시대"] = pd.cut(
        data["연도"],
        bins=[1969, 1979, 1989, 1999, 2009, 2019, 2023],
        labels=["1970년대", "1980년대", "1990년대", "2000년대", "2010년대", "2020~2023년"],
    )
    era_average = data.groupby("시대", observed=True)[
        ["출생아수(명)", "합계출산율(명)", "자연증가건수(명)"]
    ].mean()
    first_year = int(data["연도"].min())
    last_year = int(data["연도"].max())
    years_elapsed = last_year - first_year
    birth_cagr = (data["출생아수(명)"].iloc[-1] / data["출생아수(명)"].iloc[0]) ** (1 / years_elapsed) - 1
    replacement_year = data.loc[data["합계출산율(명)"] < 2.1, "연도"].iloc[0]
    natural_decrease = data.loc[data["자연증가건수(명)"] < 0, "연도"]
    first_natural_decrease_year = int(natural_decrease.iloc[0])
    decrease_years = data.loc[data["출생아수_감소여부"], "연도"].astype(int)
    longest_decrease = 0
    current_decrease = 0
    for is_decreasing in data["출생아수_감소여부"].fillna(False):
        current_decrease = current_decrease + 1 if is_decreasing else 0
        longest_decrease = max(longest_decrease, current_decrease)
    sex_ratio_change = data["출생성비(명)"].iloc[-1] - data["출생성비(명)"].iloc[0]
    recent_lowest_fertility = data.loc[data["합계출산율(명)"].idxmin(), ["연도", "합계출산율(명)"]]
    recent_lowest_natural_growth = data.loc[data["자연증가건수(명)"].idxmin(), ["연도", "자연증가건수(명)"]]

    era_average.to_csv(OUTPUT_DIR / "시대별_평균.csv", encoding="utf-8-sig")
    data[["연도", "출생아수_전년대비변화율", "출생아수_감소여부"]].to_csv(
        OUTPUT_DIR / "출생아수_연간변화.csv", index=False, encoding="utf-8-sig"
    )

    print("[데이터 클렌징]")
    print(f"행/열: {data.shape[0]}행 x {data.shape[1]}열")
    print(f"연도 범위: {data['연도'].min()}~{data['연도'].max()}")
    print(f"결측치: {int(missing.sum())}개, 중복 연도: {duplicate_years}개")
    print("수치형 변환 대상:", ", ".join(numeric_columns))

    print("\n[핵심 분석]")
    print(f"최다 출생 연도: {int(highest_birth_year['연도'])}년, {highest_birth_year['출생아수(명)']:,.0f}명")
    print(f"최저 출생 연도: {int(lowest_birth_year['연도'])}년, {lowest_birth_year['출생아수(명)']:,.0f}명")
    print(f"최근 10년 출생아 수 변화율: {decade_change['출생아수(명)'].iloc[0]:.1%}")
    print(f"최근 10년 합계출산율 변화율: {decade_change['합계출산율(명)'].iloc[0]:.1%}")
    print(f"1970→2023 출생아 수 장기 연평균 변화율(CAGR): {birth_cagr:.2%}")
    print(f"합계출산율이 인구 대체수준 2.1명 아래로 처음 내려간 해: {int(replacement_year)}년")
    print(f"자연증가건수가 처음 음수가 된 해: {first_natural_decrease_year}년")
    print(f"출생아 수 전년 대비 감소가 가장 길게 이어진 기간: {longest_decrease}년 연속")
    print(f"출생성비 변화: {sex_ratio_change:+.1f}명 ({data['출생성비(명)'].iloc[0]:.1f}→{data['출생성비(명)'].iloc[-1]:.1f})")
    print(f"최저 합계출산율: {int(recent_lowest_fertility['연도'])}년, {recent_lowest_fertility['합계출산율(명)']:.3f}명")
    print(f"최저 자연증가건수: {int(recent_lowest_natural_growth['연도'])}년, {recent_lowest_natural_growth['자연증가건수(명)']:,.0f}명")
    print("\n시대별 평균:")
    print(era_average.round(1).to_string())
    print("\n최근 10년 데이터:")
    print(recent[["출생아수(명)", "합계출산율(명)", "자연증가건수(명)"]].to_string())
    print("\n상관계수 (인과관계가 아닌 동행 정도):")
    print(correlation.to_string())
    print(f"\n결과 저장 위치: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()