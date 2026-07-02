<%*
const today = tp.date.now("YYYY-MM-DD");
const title = tp.file.title.replace(/^Vendor-/, "");
const lines = [
  `---`,
  `유형: vendor`,
  `상태: 진행중`,
  `담당: 나`,
  `관련: []`,
  `최종수정: ${today}`,
  `태그:`,
  `  - 벤더`,
  `---`,
  ``,
  `# Vendor: ${title}`,
  ``,
  `## 개요`,
  `- `,
  ``,
  `## 계약 / 수수료`,
  `| 항목 | 내용 | 기준일 |`,
  `|---|---|---|`,
  `| 수수료율 |  | ${today} |`,
  `| 정산 주기 |  | ${today} |`,
  `| 계약 상태 |  | ${today} |`,
  ``,
  `## 연동 스펙`,
  `- `,
  ``,
  `## 히스토리`,
  `- ${today} 벤더 페이지 생성.`,
];
tR += lines.join("\n");
_%>