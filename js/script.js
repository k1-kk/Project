// 获取按钮和 body 元素
const themeToggleBtn = document.getElementById('theme-toggle');
const bodyElement = document.body;

// // 绑定点击事件
// themeToggleBtn.addEventListener('click', () => {
//     // toggle() 方法会在有这个类名时移除它，没有时添加它
//     bodyElement.classList.toggle('dark-mode');
    
//     // 动态修改按钮文字
//     if (bodyElement.classList.contains('dark-mode')) {
//         themeToggleBtn.textContent = '切换白天模式';
//     } else {
//         themeToggleBtn.textContent = '切换暗黑模式';
//     }
// });

function setTheme(isDark){
    bodyElement.classList.toggle("dark-mode",isDark);
    themeToggleBtn.textContent = isDark ? '切换白天模式' : '切换暗黑模式';
    localStorage.setItem('theme',isDark ? 'dark' : 'light');
}

const savedTheme = localStorage.getItem('theme');
setTheme(savedTheme === 'dark');

themeToggleBtn.addEventListener('click',() => {
    const isDark = !bodyElement.classList.contains('dark-mode');
    setTheme(isDark);
});

const filterButtons = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-card');

filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        const filter = button.dataset.filter;

        filterButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        projectCards.forEach(card => {
            const category = card.dataset.category;

            if (filter === 'all' || category === filter) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
});

const detailButtons = document.querySelectorAll('.detail-btn');

detailButtons.forEach(button => {
    button.addEventListener('click', () => {
        const card = button.closest('.project-card');
        card.classList.toggle('open');

        button.textContent = card.classList.contains('open')
            ? '收起详情'
            : '查看详情';
    });
});