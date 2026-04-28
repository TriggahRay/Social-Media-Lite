const followBtn = document.getElementById('follow-btn');
  if (followBtn) {
    followBtn.addEventListener('click', function() {
      const username = this.dataset.username;
      fetch(`/follow/${username}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': CSRF_TOKEN,
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(r => r.json())
      .then(data => {
        if (data.is_following) {
          followBtn.textContent = 'Following';
          followBtn.classList.add('following');
        } else {
          followBtn.textContent = 'Follow';
          followBtn.classList.remove('following');
        }
        // Update follower count on the page
        document.querySelector('.stat-number:nth-child(1)').textContent = data.followers_count;
      });
    });
  }

    // Scroll to bottom of chat on load
  const chatWrapper = document.getElementById('chat-wrapper');
  chatWrapper.scrollTop = chatWrapper.scrollHeight;

  // Send message via AJAX
  function sendMessage() {
    const input = document.getElementById('msg-input');
    const content = input.value.trim();
    if (!content) return;

    fetch(`/messages/{{ other_user.username }}/send/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRF_TOKEN,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `content=${encodeURIComponent(content)}`
    })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        const m = data.message;
        chatWrapper.insertAdjacentHTML('beforeend', `
          <div class="bubble-wrapper mine">
            <div>
              <div class="bubble mine">${m.content}</div>
              <div class="bubble-time">${m.created_at}</div>
            </div>
          </div>`);
        input.value = '';
        chatWrapper.scrollTop = chatWrapper.scrollHeight;
      }
    });
  }

  // Send on Enter key
  document.getElementById('msg-input').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendMessage();
    }
  });

    // Show image preview before uploading
  function previewImage(input) {
    if (input.files && input.files[0]) {
      const reader = new FileReader();
      reader.onload = e => {
        document.getElementById('preview-img').src = e.target.result;
        document.getElementById('image-preview').style.display = 'block';
      };
      reader.readAsDataURL(input.files[0]);
    }
  }

  
  // ── Expand create post form when trigger is clicked ──
  document.getElementById('createTrigger').addEventListener('click', function() {
    document.getElementById('createForm').style.display = 'block';
    document.getElementById('postContent').focus();
    this.style.display = 'none';
  });

  // ── Character counter for post textarea ──
  document.getElementById('postContent').addEventListener('input', function() {
    document.getElementById('charCount').textContent = this.value.length;
  });

  // ── Image preview before upload ──
  document.getElementById('postImage').addEventListener('change', function() {
    if (this.files && this.files[0]) {
      const reader = new FileReader();
      reader.onload = e => {
        document.getElementById('imagePreview').src = e.target.result;
        document.getElementById('imagePreviewWrap').style.display = 'block';
      };
      reader.readAsDataURL(this.files[0]);
    }
  });

  // ── Remove selected image ──
  document.getElementById('removeImage').addEventListener('click', function() {
    document.getElementById('postImage').value = '';
    document.getElementById('imagePreviewWrap').style.display = 'none';
    document.getElementById('imagePreview').src = '';
  });

  // ── Toggle like ──
  function toggleLike(postId) {
    fetch(`/like/${postId}/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': CSRF_TOKEN }
    })
    .then(r => r.json())
    .then(data => {
      const btn   = document.getElementById(`like-btn-${postId}`);
      const icon  = btn.querySelector('i');
      const count = document.getElementById(`likes-count-${postId}`);
      if (data.liked) {
        btn.classList.add('liked');
        icon.className = 'bi bi-heart-fill';
      } else {
        btn.classList.remove('liked');
        icon.className = 'bi bi-heart';
      }
      count.textContent = data.likes_count;
    });
  }

  // ── Focus comment input ──
  function focusComment(postId) {
    document.getElementById(`comment-input-${postId}`).focus();
  }

  // ── Submit comment ──
  function submitComment(postId) {
    const input   = document.getElementById(`comment-input-${postId}`);
    const content = input.value.trim();
    if (!content) return;

    fetch(`/comment/${postId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRF_TOKEN,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `content=${encodeURIComponent(content)}`
    })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        const c   = data.comment;
        const div = document.getElementById(`comments-${postId}`);
        div.insertAdjacentHTML('beforeend', `
          <div class="comment-item">
            <div class="avatar-placeholder size-sm">
              ${c.username[0].toUpperCase()}
            </div>
            <div class="comment-body">
              <div class="comment-username">${c.username}</div>
              <div class="comment-text">${c.content}</div>
              <div class="comment-time">Just now</div>
            </div>
          </div>`);
        input.value = '';
        input.style.height = 'auto';
      }
    });
  }

  // ── Auto-resize comment textarea ──
  document.querySelectorAll('.comment-input').forEach(textarea => {
    textarea.addEventListener('input', function() {
      this.style.height = 'auto';
      this.style.height = this.scrollHeight + 'px';
    });
    textarea.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        submitComment(this.id.replace('comment-input-', ''));
      }
    });
  });

  // ── Follow / Unfollow suggested users ──
  function toggleFollow(username, btn) {
    fetch(`/follow/${username}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRF_TOKEN,
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(r => r.json())
    .then(data => {
      if (data.is_following) {
        btn.textContent = 'Following';
        btn.classList.add('following');
        // Fade out the suggested user card after following
        setTimeout(() => {
          const card = document.getElementById(`suggested-${username}`);
          if (card) {
            card.style.opacity = '0';
            card.style.transition = 'opacity 0.4s';
            setTimeout(() => card.remove(), 400);
          }
        }, 600);
      } else {
        btn.textContent = 'Follow';
        btn.classList.remove('following');
      }
    });
  }

  let lastScrollTop = 0;
let timeout;

const nav = document.querySelector('.bottom-nav');

window.addEventListener('scroll', function () {
    let currentScroll = window.pageYOffset || document.documentElement.scrollTop;

    // SCROLL DOWN → hide
    if (currentScroll > lastScrollTop) {
        nav.classList.add('hide');
    }
    // SCROLL UP → show
    else {
        nav.classList.remove('hide');
    }

    // When user STOPS scrolling → show again
    clearTimeout(timeout);
    timeout = setTimeout(() => {
        nav.classList.remove('hide');
    }, 200);

    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
});

    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    const CSRF_TOKEN = getCookie('csrftoken');

    // ── Poll notification count every 30 seconds ──
    
    function updateNotifBadge() {
      fetch("{% url 'social:notification_count' %}")
        .then(r => r.json())
        .then(data => {
          const badges = document.querySelectorAll('#notif-count, #notif-count-mobile');
          badges.forEach(badge => {
            if (data.unread_count > 0) {
              badge.textContent = data.unread_count;
              badge.classList.remove('d-none');
            } else {
              badge.classList.add('d-none');
            }
          });
        });
    }
    updateNotifBadge();
    setInterval(updateNotifBadge, 30000);

    // ── Live search ──
    const searchInput = document.getElementById('search-input');
    const searchDropdown = document.getElementById('search-dropdown');
    let searchTimer;

    if (searchInput) {
      searchInput.addEventListener('input', function() {
        clearTimeout(searchTimer);
        const q = this.value.trim();
        if (q.length < 2) {
          searchDropdown.classList.remove('show');
          return;
        }
        searchTimer = setTimeout(() => {
          fetch(`{% url 'messaging:search' %}?q=${encodeURIComponent(q)}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
          })
          .then(r => r.json())
          .then(data => {
            let html = '';
            if (data.users.length > 0) {
              html += `<div class="search-section-title">People</div>`;
              data.users.forEach(u => {
                html += `
                  <a href="/accounts/profile/${u.username}/" class="search-result-item">
                    <div class="avatar-placeholder size-sm">${u.username[0].toUpperCase()}</div>
                    <div>
                      <div style="font-weight:600;font-size:0.88rem;">@${u.username}</div>
                      <div style="font-size:0.78rem;color:var(--text-secondary);">${u.bio.substring(0,40)}</div>
                    </div>
                  </a>`;
              });
            }
            if (data.posts.length > 0) {
              html += `<div class="search-section-title">Posts</div>`;
              data.posts.forEach(p => {
                html += `
                  <a href="/accounts/post/${p.id}/" class="search-result-item">
                    <i class="bi bi-file-text" style="color:var(--accent);font-size:1.1rem;"></i>
                    <div>
                      <div style="font-size:0.88rem;">${p.content}</div>
                      <div style="font-size:0.78rem;color:var(--text-secondary);">by @${p.username}</div>
                    </div>
                  </a>`;
              });
            }
            if (!html) html = `<div class="search-result-item" style="color:var(--text-muted);">No results found</div>`;
            searchDropdown.innerHTML = html;
            searchDropdown.classList.add('show');
          });
        }, 300);
      });

      // Close dropdown when clicking outside
      document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target)) {
          searchDropdown.classList.remove('show');
        }
      });
    }
