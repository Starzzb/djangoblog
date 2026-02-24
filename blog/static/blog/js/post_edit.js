/**
 * Post Edit Page Scripts — 写文章/编辑页脚本
 * 自动为表单控件添加样式类
 */
document.addEventListener('DOMContentLoaded', function () {
    // 为所有 input、textarea、select 添加 form-control 类
    document.querySelectorAll('input, textarea, select').forEach(function (element) {
        if (element.type !== 'submit' && element.type !== 'file') {
            element.classList.add('form-control');
        }
    });
});
