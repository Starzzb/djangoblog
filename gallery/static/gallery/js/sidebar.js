// sidebar.js 优化版
document.addEventListener('DOMContentLoaded', function () {
  const sidebarDrawer = document.getElementById('sidebarDrawer');
  const sidebarBackdrop = document.getElementById('sidebarBackdrop');
  const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');

  function toggleSidebar() {
    const isOpen = sidebarDrawer.classList.contains('show');
    if (isOpen) {
      closeSidebar();
    } else {
      openSidebar();
    }
  }

  function openSidebar() {
    sidebarDrawer.classList.add('show');
    sidebarBackdrop.classList.add('show');
    document.body.classList.add('sidebar-open');
    // 移动端处理
    if (window.innerWidth <= 768) {
      document.body.style.overflow = 'hidden';
    }
  }

  function closeSidebar() {
    sidebarDrawer.classList.remove('show');
    sidebarBackdrop.classList.remove('show');
    document.body.classList.remove('sidebar-open');
    // 明确设置overflow
    document.body.style.overflowY = 'auto';
    document.body.style.overflowX = 'hidden';
  }

  // 点击遮罩关闭
  sidebarBackdrop.addEventListener('click', closeSidebar);

  // 点击按钮切换
  sidebarToggleBtn.addEventListener('click', toggleSidebar);

  // ESC键关闭
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && sidebarDrawer.classList.contains('show')) {
      closeSidebar();
    }
  });
});
// 添加到sidebar.js末尾，确保DOM加载完成后再初始化粒子
