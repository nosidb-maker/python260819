$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$out = Join-Path $root '출생아_분석.pptx'
$chart = Join-Path $root '출생아수_분석결과\연도별_출생아수_라인그래프.png'

$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = -1
$presentation = $ppt.Presentations.Add()
$presentation.PageSetup.SlideWidth = 13.333 * 72
$presentation.PageSetup.SlideHeight = 7.5 * 72
$blank = 12
$dark = 0x172B4D
$teal = 0x006B73
$gold = 0xA96F00
$red = 0x9C2F2A
$ink = 0x243447
$muted = 0x405466
$pale = 0xEAF1F3
$white = 0xFFFFFF
$pointsPerInch = 72

function P($inches) {
    return [float]$inches * $pointsPerInch
}

function Add-Text($slide, $text, $left, $top, $width, $height, $size, $color, $bold = $False, $align = 1) {
    $box = $slide.Shapes.AddTextbox(1, (P $left), (P $top), (P $width), (P $height))
    $cleanText = [string]$text -replace '\\n', [Environment]::NewLine
    $box.TextFrame.TextRange.Text = $cleanText
    $box.TextFrame.TextRange.Font.Name = '맑은 고딕'
    $box.TextFrame.TextRange.Font.Size = $size
    $box.TextFrame.TextRange.Font.Bold = $bold
    $box.TextFrame.TextRange.Font.Color.RGB = $color
    $box.TextFrame.TextRange.ParagraphFormat.Alignment = $align
    $box.TextFrame.VerticalAnchor = 3
    $box.TextFrame.MarginLeft = 5
    $box.TextFrame.MarginRight = 5
    return $box
}

function Add-Header($slide, $title, $subtitle = '') {
    $slide.Background.Fill.ForeColor.RGB = $white
    $bar = $slide.Shapes.AddShape(1, (P 0), (P 0), (P 13.333), (P 0.16))
    $bar.Fill.ForeColor.RGB = $teal
    $bar.Line.Visible = 0
    Add-Text $slide $title 0.55 0.42 12.2 0.45 25 $dark $True 1 | Out-Null
    if ($subtitle -ne '') { Add-Text $slide $subtitle 0.58 0.91 11.7 0.28 10 $muted $False 1 | Out-Null }
}

function Add-Footer($slide, $page) {
    Add-Text $slide '자료: 통계청 인구동향조사 / KOSIS, 1970~2023' 0.55 7.13 8.5 0.18 8 $muted | Out-Null
    Add-Text $slide "$page" 12.35 7.1 0.35 0.2 9 $muted $True 3 | Out-Null
}

function Add-Card($slide, $label, $value, $note, $left, $top, $width, $accent) {
    $card = $slide.Shapes.AddShape(5, (P $left), (P $top), (P $width), (P 1.2))
    $card.Fill.ForeColor.RGB = $pale
    $card.Line.ForeColor.RGB = 0xD8E4E7
    $stripe = $slide.Shapes.AddShape(1, (P $left), (P $top), (P 0.08), (P 1.2))
    $stripe.Fill.ForeColor.RGB = $accent
    $stripe.Line.Visible = 0
    Add-Text $slide $label ($left + 0.18) ($top + 0.13) ($width - 0.3) 0.22 10 $muted | Out-Null
    Add-Text $slide $value ($left + 0.18) ($top + 0.39) ($width - 0.3) 0.38 23 $dark $True | Out-Null
    Add-Text $slide $note ($left + 0.18) ($top + 0.86) ($width - 0.3) 0.18 9 $muted | Out-Null
}

# 1. 표지
$slide = $presentation.Slides.Add($presentation.Slides.Count + 1, $blank)
$slide.Background.Fill.ForeColor.RGB = $dark
$accent = $slide.Shapes.AddShape(1, (P 0), (P 0), (P 13.333), (P 0.2))
$accent.Fill.ForeColor.RGB = $gold; $accent.Line.Visible = 0
Add-Text $slide '출생아 분석' 0.78 1.2 11.7 0.75 42 $white $True 1 | Out-Null
Add-Text $slide '대한민국 인구구조 변화와 정책 대응 방향' 0.82 2.1 11.3 0.38 20 0xDDE9EA | Out-Null
$rule = $slide.Shapes.AddShape(1, (P 0.82), (P 2.75), (P 2.2), (P 0.06)); $rule.Fill.ForeColor.RGB = $gold; $rule.Line.Visible = 0
Add-Text $slide '1970~2023년 KOSIS 데이터 기반' 0.82 3.05 6.5 0.3 13 0xDDE9EA | Out-Null
Add-Text $slide '대통령 보고용 정책 브리핑' 0.82 6.45 5.5 0.28 11 0xAFC4C8 | Out-Null
Add-Text $slide '2026. 08.' 11.25 6.45 1.3 0.28 11 0xAFC4C8 $False 3 | Out-Null

# 2. 핵심 요약
$slide = $presentation.Slides.Add($presentation.Slides.Count + 1, $blank)
Add-Header $slide '핵심 요약' '출생·출산·자연증가가 동시에 악화되는 구조적 전환'
Add-Card $slide '2023년 출생아 수' '23.0만 명' '1971년 정점 대비 -77.6%' 0.65 1.45 3.0 $teal
Add-Card $slide '2023년 합계출산율' '0.720명' '1983년 대체수준 2.1명 하회 시작' 3.88 1.45 3.0 $gold
Add-Card $slide '자연증가건수' '-12.3만 명' '2020년부터 자연감소 전환' 7.11 1.45 3.0 $red
Add-Text $slide '대통령께 드리는 4가지 판단' 0.7 3.05 4.0 0.3 15 $dark $True | Out-Null
Add-Text $slide "• 출생 규모는 50년 이상 누적 하락해 단기 반등만으로 되돌리기 어렵다.\n• 합계출산율 하락과 자연감소가 함께 진행되어 인구정책의 시간축이 길다.\n• 최근 10년 출생아 수 -47.3%, 합계출산율 -39.3%로 감소 속도가 빠르다.\n• 회복 정책과 인구감소 적응을 동시에 추진해야 한다." 0.78 3.48 11.2 1.65 16 $ink | Out-Null
$call = $slide.Shapes.AddShape(5, (P 0.78), (P 5.55), (P 11.55), (P 0.72)); $call.Fill.ForeColor.RGB = 0xFFF4D9; $call.Line.ForeColor.RGB = $gold
Add-Text $slide '보고 판단' 1.0 5.68 1.1 0.25 12 $gold $True | Out-Null
Add-Text $slide '결론: 출산율 회복과 인구감소 적응을 한 정책 패키지로 관리해야 한다.' 2.15 5.67 9.8 0.27 14 $dark $True | Out-Null
Add-Footer $slide 2

# 3. 장기 추세
$slide = $presentation.Slides.Add($presentation.Slides.Count + 1, $blank)
Add-Header $slide '장기 추세: 출생 규모의 구조적 축소' '1970년대의 백만 명대 출생에서 2023년 23만 명으로 하락'
$slide.Shapes.AddPicture($chart, $False, $True, (P 0.65), (P 1.35), (P 7.6), (P 4.85)) | Out-Null
Add-Text $slide '수치로 본 변화' 8.65 1.55 3.5 0.3 15 $dark $True | Out-Null
Add-Text $slide '1971년 정점\n1,024,773명' 8.7 2.05 3.7 0.72 22 $teal $True | Out-Null
Add-Text $slide '2023년 최저\n230,000명' 8.7 3.05 3.7 0.72 22 $red $True | Out-Null
Add-Text $slide '장기 연평균 변화율(CAGR)\n-2.75%' 8.7 4.1 3.7 0.72 22 $gold $True | Out-Null
Add-Text $slide '출생아 수 감소는 일시적 변동이 아니라 50년 이상 누적된 추세다.' 8.7 5.25 3.65 0.55 13 $ink | Out-Null
Add-Footer $slide 3

# 4. 시대별 비교
$slide = $presentation.Slides.Add($presentation.Slides.Count + 1, $blank)
Add-Header $slide '시대별 비교: 저출산에서 자연감소로' '평균값 기준으로 본 인구구조의 단계적 악화'
$table = $slide.Shapes.AddTable(7, 4, (P 0.65), (P 1.45), (P 7.45), (P 4.7)).Table
$headers = @('시대', '평균 출생아 수', '평균 합계출산율', '평균 자연증가')
for ($c = 1; $c -le 4; $c++) { $table.Cell(1, $c).Shape.TextFrame.TextRange.Text = $headers[$c - 1] }
$rows = @(
    @('1970년대', '89.8만 명', '3.6명', '64.8만 명'),
    @('1980년대', '72.1만 명', '1.9명', '47.6만 명'),
    @('1990년대', '68.7만 명', '1.6명', '44.5만 명'),
    @('2000년대', '49.7만 명', '1.2명', '25.0만 명'),
    @('2010년대', '41.3만 명', '1.2명', '13.8만 명'),
    @('2020~2023년', '25.3만 명', '0.8명', '-8.4만 명')
)
for ($r = 0; $r -lt $rows.Count; $r++) { for ($c = 0; $c -lt 4; $c++) { $table.Cell($r + 2, $c + 1).Shape.TextFrame.TextRange.Text = $rows[$r][$c] } }
for ($r = 1; $r -le 7; $r++) { for ($c = 1; $c -le 4; $c++) { $cell = $table.Cell($r, $c); $cell.Shape.TextFrame.TextRange.Font.Name = '맑은 고딕'; $cell.Shape.TextFrame.TextRange.Font.Size = 12; $cell.Shape.TextFrame.TextRange.Font.Color.RGB = $ink; $cell.Shape.Fill.ForeColor.RGB = $(if ($r -eq 1) { $dark } elseif ($r -eq 7) { 0xFCE9E7 } elseif ($r % 2 -eq 0) { $pale } else { $white }); if ($r -eq 1) { $cell.Shape.TextFrame.TextRange.Font.Color.RGB = $white; $cell.Shape.TextFrame.TextRange.Font.Bold = $True } } }
Add-Text $slide '해석' 8.65 1.6 2.0 0.3 15 $dark $True | Out-Null
Add-Text $slide '• 1980년대부터 이미 대체수준 아래\n• 2000년대 이후 출생 규모가 빠르게 축소\n• 2020년대 평균 자연증가건수는 음수\n• 출산율 하락이 출생아 수와 자연증가 감소로 연결' 8.65 2.15 3.8 2.5 16 $ink | Out-Null
$call = $slide.Shapes.AddShape(5, (P 8.65), (P 5.15), (P 3.65), (P 0.85)); $call.Fill.ForeColor.RGB = 0xE5F3F4; $call.Line.ForeColor.RGB = $teal
Add-Text $slide '전환점: 2020년 자연감소 진입' 8.85 5.38 3.2 0.25 14 $teal $True | Out-Null
Add-Footer $slide 4

# 5. 출산율과 자연증가
$slide = $presentation.Slides.Add($presentation.Slides.Count + 1, $blank)
Add-Header $slide '출산율과 자연증가: 인구감소가 이미 시작됨' '출생아 수만의 문제가 아니라 인구 재생산 구조의 문제'
Add-Card $slide '대체수준 하회 시작' '1983년' '합계출산율 2.1명 미만' 0.7 1.45 3.25 $gold
Add-Card $slide '자연감소 전환' '2020년' '자연증가건수 0 미만' 4.25 1.45 3.25 $red
Add-Card $slide '최저 자연증가' '-12.4만 명' '2022년 기록' 7.8 1.45 3.25 $red
Add-Text $slide '출생아 수와 주요 지표의 동행 관계' 0.75 3.15 5.8 0.3 15 $dark $True | Out-Null
Add-Text $slide '출생아 수 ↔ 합계출산율       r = 0.895\n출생아 수 ↔ 자연증가건수       r = 0.995\n출생아 수 ↔ 조출생률           r = 0.979' 0.8 3.7 5.8 1.35 19 $ink | Out-Null
Add-Text $slide '상관계수는 같은 방향으로 움직이는 정도를 나타내며, 정책 효과의 인과관계를 뜻하지 않는다.' 0.8 5.45 6.3 0.48 11 $muted | Out-Null
Add-Text $slide '정책적 의미' 7.95 3.15 2.7 0.3 15 $dark $True | Out-Null
Add-Text $slide '• 출산율 회복 없이는 출생 규모 반등이 어렵다.\n• 자연감소는 출생아 수 정책과 별도로 적응 전략이 필요하다.\n• 정책 평가는 출생 건수뿐 아니라 지속성·양육부담·지역 격차를 함께 봐야 한다.' 8.0 3.7 4.35 2.05 16 $ink | Out-Null
Add-Footer $slide 5

# 6. 최근 위기
$slide = $presentation.Slides.Add($presentation.Slides.Count + 1, $blank)
Add-Header $slide '최근 10년: 감소 속도가 더 빨라짐' '2014년부터 2023년까지의 최신 구간을 별도로 점검'
$years = @('2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023')
$values = @(435435, 438420, 406243, 357771, 326822, 302676, 272337, 260562, 249186, 230000)
$maxValue = 450000
for ($i = 0; $i -lt $years.Count; $i++) {
    $x = 0.8 + ($i * 0.78)
    $height = 3.35 * ($values[$i] / $maxValue)
    $bar = $slide.Shapes.AddShape(1, (P $x), (P (5.55 - $height)), (P 0.48), (P $height))
    $bar.Fill.ForeColor.RGB = $(if ($i -eq 0) { $teal } elseif ($i -eq 9) { $red } else { 0x8CC4C9 })
    $bar.Line.Visible = 0
    Add-Text $slide $years[$i] ($x - 0.12) 5.68 0.72 0.2 8 $muted $False 2 | Out-Null
}
Add-Text $slide '2014' 0.8 1.45 1.0 0.28 14 $teal $True | Out-Null
Add-Text $slide '43.5만 명' 1.65 1.43 1.6 0.3 19 $dark $True | Out-Null
Add-Text $slide '→' 3.4 1.42 0.5 0.3 20 $muted $True 2 | Out-Null
Add-Text $slide '2023' 4.15 1.45 1.0 0.28 14 $red $True | Out-Null
Add-Text $slide '23.0만 명' 5.0 1.43 1.6 0.3 19 $dark $True | Out-Null
Add-Text $slide '최근 10년 변화율: -47.3%' 8.0 1.48 4.0 0.35 22 $red $True | Out-Null
Add-Text $slide '2015년의 소폭 반등 이후 2023년까지 8년 연속 감소.\n단기 경기 변동보다 구조적 요인의 영향이 큰 구간으로 해석된다.' 8.0 2.2 4.15 1.2 16 $ink | Out-Null
Add-Text $slide '※ 막대는 출생아 수(명), 축약 표기는 만 명 단위' 0.8 6.2 4.0 0.2 9 $muted | Out-Null
Add-Footer $slide 6

# 7. 정책 시사점
$slide = $presentation.Slides.Add($presentation.Slides.Count + 1, $blank)
Add-Header $slide '정책 시사점 및 보고 제안' '데이터가 말하는 우선순위: 회복과 적응을 동시에'
$items = @(
    @('01', '출산·양육 비용의 실질 부담 완화', '주거·돌봄·교육비를 생애주기 관점에서 묶어 체감 가능한 지원으로 설계'),
    @('02', '청년의 가족 형성 기반 강화', '고용 안정, 주거 접근성, 일·생활 양립을 출산 결정 이전부터 점검'),
    @('03', '지역별 맞춤 전략', '전국 평균만 보지 말고 지역별 출생·이동·돌봄 인프라를 연계해 설계'),
    @('04', '자연감소 적응 병행', '인구감소를 전제로 교육·의료·연금·지역 서비스의 규모와 전달체계를 재설계')
)
for ($i = 0; $i -lt $items.Count; $i++) {
    $y = 1.4 + ($i * 1.18)
    $circle = $slide.Shapes.AddShape(9, (P 0.75), (P ($y + 0.1)), (P 0.55), (P 0.55)); $circle.Fill.ForeColor.RGB = $(if ($i -lt 2) { $teal } else { $gold }); $circle.Line.Visible = 0
    Add-Text $slide $items[$i][0] 0.78 ($y + 0.22) 0.48 0.16 9 $white $True 2 | Out-Null
    Add-Text $slide $items[$i][1] 1.55 $y 5.0 0.3 17 $dark $True | Out-Null
    Add-Text $slide $items[$i][2] 1.55 ($y + 0.38) 10.4 0.3 12 $muted | Out-Null
}
$closing = $slide.Shapes.AddShape(5, (P 0.75), (P 6.15), (P 11.55), (P 0.48)); $closing.Fill.ForeColor.RGB = $dark; $closing.Line.Visible = 0
Add-Text $slide '결론: 출산율 반등의 시간축은 길다. 지금은 회복 정책과 인구감소 대응을 함께 집행할 시점이다.' 1.0 6.27 11.05 0.18 13 $white $True 2 | Out-Null
Add-Footer $slide 7

# 8. 성과관리 및 데이터 유의사항
$slide = $presentation.Slides.Add($presentation.Slides.Count + 1, $blank)
Add-Header $slide '정책 성과관리: 숫자 하나가 아닌 세 축으로 점검' '출생아 수의 단기 변동보다 지속 가능한 가족 형성 환경을 측정'
Add-Card $slide '회복 지표' '합계출산율' '연도별 수준과 반등의 지속성' 0.7 1.45 3.3 $teal
Add-Card $slide '부담 지표' '주거·돌봄 부담' '청년·신혼·양육가구 체감도' 4.25 1.45 3.3 $gold
Add-Card $slide '적응 지표' '지역 인구감소' '교육·의료·돌봄 서비스 접근성' 7.8 1.45 3.3 $red
Add-Text $slide '보고 시 함께 명시할 유의사항' 0.78 3.15 4.8 0.3 15 $dark $True | Out-Null
Add-Text $slide '• 본 보고서는 KOSIS 통계표의 1970~2023년 관측자료를 분석한 결과다.\n• 2023년 값은 원자료의 잠정 표기(p)를 유지해 연도만 정규화했다.\n• 상관계수는 동행 정도이며 특정 정책의 인과효과를 추정한 결과가 아니다.\n• 정책 효과 평가는 출생아 수뿐 아니라 결혼·출산 의향, 실제 부담, 지역 격차를 함께 추적해야 한다.' 0.8 3.62 11.3 1.6 16 $ink | Out-Null
$note = $slide.Shapes.AddShape(5, (P 0.78), (P 5.65), (P 11.55), (P 0.75)); $note.Fill.ForeColor.RGB = $dark; $note.Line.Visible = 0
Add-Text $slide '대통령 지시 제안' 1.0 5.84 1.8 0.22 12 0xFFFFFF $True | Out-Null
Add-Text $slide '관계부처는 회복·부담·적응 3개 축의 연차 목표와 예산 연계를 제시하고, 매년 동일 지표로 성과를 보고한다.' 2.75 5.82 9.1 0.28 14 0xFFFFFF $True | Out-Null
Add-Footer $slide 8

$presentation.SaveAs($out)
$presentation.Close()
$ppt.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($presentation) | Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
Write-Output "Created: $out"