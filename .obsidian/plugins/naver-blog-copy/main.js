const { Plugin, Notice } = require('obsidian');
const { clipboard } = require('electron');

module.exports = class NaverBlogCopy extends Plugin {
  onload() {
    this.addCommand({
      id: 'copy-selection', name: 'Copy selection for Naver Blog',
      editorCallback: (editor) => {
        const source = editor.getSelection();
        if (!source.trim()) { new Notice('복사할 본문을 먼저 선택하세요.'); return; }
        const escape = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        const inline = s => escape(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        const lines = source.replace(/\r\n?/g, '\n').split('\n');
        let html = '';
        for (const line of lines) {
          if (!line.trim()) { html += '<p><br></p>'; continue; }
          const heading = line.trim().match(/^<div\s+style=["']([^"']*(?:["'][^"']*["'][^"']*)*)["']>(.*?)<\/div>$/i);
          if (heading) { html += '<p style="font-size:24pt;font-weight:700;font-family:NanumMyeongjo,serif">' + inline(heading[2]) + '</p>'; continue; }
          const mdHeading = line.match(/^(#{1,6})\s+(.+)$/);
          if (mdHeading) { html += '<h' + mdHeading[1].length + '>' + inline(mdHeading[2]) + '</h' + mdHeading[1].length + '>'; continue; }
          html += '<p>' + inline(line.trim()) + '</p>';
        }
        clipboard.write({html, text: source});
        new Notice('네이버 블로그용으로 복사했습니다. 블로그에서 붙여 넣으세요.');
      }
    });
  }
};
