// static/js/favorite.js
document.addEventListener('DOMContentLoaded', function () {
    // 初始化所有收藏按钮的状态
    initializeFavoriteButtons();

    // 为所有收藏按钮添加点击事件
    document.querySelectorAll('.favorite-btn').forEach(button => {
        button.addEventListener('click', toggleFavorite);
    });

    // 初始化剪贴板功能
    initializeClipboard();
});

/**
 * 初始化收藏按钮状态
 */
function initializeFavoriteButtons() {
    const favoriteIcons = document.querySelectorAll('.favorite-icon');

    favoriteIcons.forEach(icon => {
        const artworkId = parseInt(icon.getAttribute('data-artwork-id'));
        if (artworkId) {
            updateFavoriteStatus(artworkId, icon);
        }
    });
}

/**
 * 更新单个收藏按钮的状态
 */
async function updateFavoriteStatus(artworkId, iconElement) {
    try {
        const response = await fetch(`/gallery/api/favorite/status/${artworkId}/`);
        const data = await response.json();

        if (data.is_favorited) {
            iconElement.classList.add('favorited');
            iconElement.parentElement.setAttribute('aria-label', '取消收藏');
        } else {
            iconElement.classList.remove('favorited');
            iconElement.parentElement.setAttribute('aria-label', '添加收藏');
        }
    } catch (error) {
        console.error('Failed to update favorite status:', error);
    }
}

/**
 * 获取 CSRF token
 */
function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='));
    if (cookieValue) {
        return cookieValue.split('=')[1];
    }
    // 也可以从 meta 标签或隐藏 input 获取
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfInput) {
        return csrfInput.value;
    }
    return '';
}

/**
 * 切换收藏状态
 */
async function toggleFavorite(event) {
    event.preventDefault();
    event.stopPropagation();

    const button = event.currentTarget;
    const icon = button.querySelector('.favorite-icon');
    const artworkId = parseInt(icon.getAttribute('data-artwork-id'));

    if (!artworkId) {
        showError('无效的作品ID');
        return;
    }

    // 显示加载状态
    button.classList.add('loading');

    try {
        const response = await fetch(`/gallery/favorite/${artworkId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            }
        });

        const data = await response.json();

        if (data.success) {
            // 切换收藏状态
            icon.classList.toggle('favorited');

            // 更新按钮标签
            if (icon.classList.contains('favorited')) {
                button.setAttribute('aria-label', '取消收藏');
                showSuccess('已添加到收藏');
            } else {
                button.setAttribute('aria-label', '添加收藏');
                showSuccess('已取消收藏');

                // 如果是在收藏页面，取消收藏后移除该卡片
                if (window.location.pathname === '/gallery/favorites/') {
                    const card = button.closest('.col');
                    if (card) {
                        requestAnimationFrame(() => {
                            card.style.transition = 'all 0.3s ease';
                            card.style.opacity = '0';
                            card.style.transform = 'scale(0.9)';
                            setTimeout(() => {
                                card.remove();
                                const allCards = document.querySelectorAll('.gallery-card');
                                if (allCards.length === 0) {
                                    location.reload();
                                }
                            }, 300);
                        });
                    }
                }
            }
        } else {
            showError(data.error || '操作失败');
        }
    } catch (error) {
        console.error('Error toggling favorite:', error);
        showError('网络错误，请重试');
    } finally {
        // 移除加载状态
        button.classList.remove('loading');
    }
}

/**
 * 显示成功消息
 */
function showSuccess(message) {
    createAlert(message, 'success');
}

/**
 * 显示错误消息
 */
function showError(message) {
    createAlert(message, 'danger');
}

/**
 * 创建并显示提示框
 */
function createAlert(message, type) {
    // 移除已存在的提示框
    const existingAlerts = document.querySelectorAll('.alert.fixed-top');
    existingAlerts.forEach(alert => alert.remove());

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show fixed-top`;
    alertDiv.style.top = '70px';
    alertDiv.style.right = '20px';
    alertDiv.style.left = 'auto';
    alertDiv.style.width = '300px';
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(alertDiv);

    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 3000);
}

/**
 * 初始化剪贴板功能
 */
function initializeClipboard() {
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const textToCopy = this.getAttribute('data-clipboard-text');
            copyToClipboard(textToCopy, this);
        });
    });
}

async function copyToClipboard(text, button) {
    try {
        await navigator.clipboard.writeText(text);
        showCopyFeedback(button);
    } catch (err) {
        fallbackCopyTextToClipboard(text, button);
    }
}

function fallbackCopyTextToClipboard(text, button) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
    textArea.style.opacity = "0";

    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showCopyFeedback(button);
        } else {
            showError('复制失败，请手动复制');
        }
    } catch (err) {
        showError('复制失败，请手动复制');
    }

    document.body.removeChild(textArea);
}

function showCopyFeedback(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-check"></i> 已复制';
    button.classList.add('btn-success');
    button.classList.remove('btn-outline-secondary');

    setTimeout(() => {
        button.innerHTML = originalText;
        button.classList.remove('btn-success');
        button.classList.add('btn-outline-secondary');
    }, 2000);
}