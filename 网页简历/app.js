/* 刘洋 · 产品经理简历 —— 交互与渲染逻辑 */
(function () {
  'use strict';
  var D = window.PM_DATA;
  if (!D) { console.error('[Resume] PM_DATA not loaded!'); return; }
  var P = D.personal;

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  // Hero avatar
  var heroAvatar = document.getElementById('hero-avatar');
  if (heroAvatar) {
    var avImg = new Image();
    avImg.onload = function () { heroAvatar.classList.add('has-photo'); };
    avImg.onerror = function () { heroAvatar.classList.add('has-photo'); };
    avImg.src = 'assets/avatar.jpg';
  }





  // Hero contact info
  var contact = document.getElementById('hero-contact');
  if (contact) {
    [[P.location], [P.birth], [P.phone], [P.email]].forEach(function (row) {
      contact.appendChild(el('li', null, row[0]));
    });
  }

  // Stats
  var statList = document.getElementById('stat-list');
  if (statList) {
    D.stats.forEach(function (s) {
      var wrap = el('div', 'stat-item');
      var num = el('span', 'stat-num', s.num);
      var label = el('span', 'stat-label', s.label);
      wrap.appendChild(num);
      wrap.appendChild(label);
      statList.appendChild(wrap);
    });
  }

  // About
  var about = document.getElementById('about-grid');
  if (about) {
    D.evaluation.forEach(function (e) {
      var card = el('article', 'about-card reveal');
      card.appendChild(el('h3', null, e.title));
      card.appendChild(el('p', null, e.desc));
      about.appendChild(card);
    });
  }

  // Timeline
  var tl = document.getElementById('timeline');
  if (tl) {
    D.work.forEach(function (w) {
      var item = el('li', 'timeline-item reveal');
      var body = el('div', 'timeline-body');
      body.appendChild(el('div', 'timeline-period', w.period));
      body.appendChild(el('h3', null, w.company));
      body.appendChild(el('p', 'timeline-role', w.role));
      if (w.project) {
        body.appendChild(el('p', 'timeline-project', '项目背景：' + w.project));
      }
      var ul = el('ul');
      w.points.forEach(function (pt) { ul.appendChild(el('li', null, pt)); });
      body.appendChild(ul);
      item.appendChild(body);
      tl.appendChild(item);
    });
  }

  // Projects
  var grid = document.getElementById('project-grid');
  var filterBar = document.getElementById('filter-bar');
  var emptyTip = document.getElementById('grid-empty');
  var CATS = ['全部', '建管项目', '灌区水利', '水务', '区县水利'];

  function countByCat(cat) {
    return cat === '全部' ? D.projects.length : D.projects.filter(function (p) { return p.category === cat; }).length;
  }

  function projectCard(proj) {
    var card = el('article', 'project-card reveal');
    card.setAttribute('data-cat', proj.category);
    card.setAttribute('data-id', proj.id);
    var top = el('div', 'proj-top');
    top.appendChild(el('span', 'proj-cat', proj.category));
    top.appendChild(el('span', 'proj-period', proj.period || ''));
    card.appendChild(top);
    card.appendChild(el('h3', 'proj-name', proj.name));
    card.appendChild(el('p', 'proj-type', proj.type));
    card.appendChild(el('p', 'proj-one', proj.oneLine || ''));
    var tags = el('div', 'proj-tags');
    (proj.tags || []).forEach(function (t) { tags.appendChild(el('span', null, t)); });
    card.appendChild(tags);
    return card;
  }

  function renderProjects(cat) {
    if (!grid) return;
    grid.innerHTML = '';
    var list = cat === '全部' ? D.projects : D.projects.filter(function (p) { return p.category === cat; });
    list.forEach(function (proj) { grid.appendChild(projectCard(proj)); });
    if (emptyTip) emptyTip.hidden = list.length > 0;
    observeReveals();
    document.querySelectorAll('.reveal').forEach(function (n) { n.classList.add('is-visible'); });
    document.querySelectorAll('.project-card').forEach(function (card) {
      card.addEventListener('click', function () {
        openProjectModal(card.getAttribute('data-id'));
      });
    });
  }

  function openProjectModal(id) {
    var proj = D.projects.find(function (p) { return p.id === id; });
    if (!proj) return;
    var overlay = document.getElementById('proj-overlay');
    if (!overlay) return;
    var modal = overlay.querySelector('.proj-modal');
    modal.innerHTML = '';
    var header = el('div', 'proj-modal-header');
    var top = el('div', 'proj-top');
    top.appendChild(el('span', 'proj-cat', proj.category));
    top.appendChild(el('span', 'proj-period', proj.period || ''));
    header.appendChild(top);
    header.appendChild(el('h2', null, proj.name));
    header.appendChild(el('p', 'proj-type', proj.type));
    modal.appendChild(header);
    var body = el('div', 'proj-modal-body');
    if (proj.background && proj.background.length) {
      body.appendChild(el('h4', null, '项目背景'));
      var ul = el('ul');
      proj.background.forEach(function (t) { ul.appendChild(el('li', null, t)); });
      body.appendChild(ul);
    }
    if (proj.actions && proj.actions.length) {
      body.appendChild(el('h4', null, '我的职责'));
      var ul = el('ul');
      proj.actions.forEach(function (t) { ul.appendChild(el('li', null, t)); });
      body.appendChild(ul);
    }
    if (proj.results && proj.results.length) {
      body.appendChild(el('h4', null, '项目成果'));
      var ul = el('ul');
      proj.results.forEach(function (t) { ul.appendChild(el('li', null, t)); });
      body.appendChild(ul);
    }
    if (proj.metrics && proj.metrics.length) {
      body.appendChild(el('h4', null, '关键数据'));
      var ul = el('ul');
      proj.metrics.forEach(function (t) { ul.appendChild(el('li', null, t)); });
      body.appendChild(ul);
    }
    var tags = el('div', 'proj-modal-tags');
    (proj.tags || []).forEach(function (t) { tags.appendChild(el('span', null, t)); });
    body.appendChild(tags);
    modal.appendChild(body);
    var closeBtn = el('button', null, '×');
    closeBtn.className = 'proj-modal-close';
    closeBtn.addEventListener('click', closeProjectModal);
    modal.insertBefore(closeBtn, modal.firstChild);
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeProjectModal() {
    var overlay = document.getElementById('proj-overlay');
    if (!overlay) return;
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  var overlay = document.getElementById('proj-overlay');
  if (overlay) {
    overlay.addEventListener('click', function (e) {
      if (e.target === this) closeProjectModal();
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeProjectModal();
  });

  if (filterBar) {
    CATS.forEach(function (cat) {
      var btn = el('button', 'filter-btn', cat);
      btn.type = 'button';
      btn.setAttribute('aria-pressed', String(cat === '全部'));
      btn.appendChild(el('span', 'count', String(countByCat(cat))));
      btn.addEventListener('click', function () {
        filterBar.querySelectorAll('.filter-btn').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
        btn.setAttribute('aria-pressed', 'true');
        renderProjects(cat);
      });
      filterBar.appendChild(btn);
    });
  }
  renderProjects('全部');

  // Mobile nav
  var toggle = document.getElementById('nav-toggle');
  var navLinks = document.getElementById('nav-links');
  if (toggle && navLinks) {
    toggle.addEventListener('click', function () {
      var open = navLinks.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    navLinks.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        navLinks.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Scroll reveal
  var io = null;
  function observeReveals() {
    if (!('IntersectionObserver' in window)) {
      document.querySelectorAll('.reveal').forEach(function (n) { n.classList.add('is-visible'); });
      return;
    }
    if (!io) {
      io = new IntersectionObserver(function (entries) { entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-visible'); } }); }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    }
    document.querySelectorAll('.reveal:not(.is-visible)').forEach(function (n) { io.observe(n); });
  }

  // Typing effect
  var heroSubEl = document.getElementById('hero-sub');
  if (heroSubEl) {
    var text = P.summary;
    var i = 0;
    // 自适应速度：长文本不至于打字太久（总时长约 2.5s 内）
    var delay = Math.max(8, Math.min(18, Math.round(2500 / Math.max(1, text.length))));
    function type() {
      if (i < text.length) {
        heroSubEl.textContent += text.charAt(i);
        i++;
        setTimeout(type, delay);
      }
    }
    type();
  }

  // Skills - 左栏：能力分组
  var abilityList = document.getElementById('ability-list');
  if (abilityList) {
    D.abilities.forEach(function (g) {
      var box = el('div', 'ability-group reveal');
      box.appendChild(el('h3', null, g.group));
      var ul = el('ul');
      g.items.forEach(function (it) { ul.appendChild(el('li', null, it)); });
      box.appendChild(ul);
      abilityList.appendChild(box);
    });
  }

  // Skills - 右栏：证书 + 教育
  var certList = document.getElementById('cert-list');
  if (certList) {
    P.certificates.forEach(function (c) { certList.appendChild(el('li', null, c)); });
  }
  var eduCard = document.getElementById('edu-card');
  if (eduCard) {
    eduCard.appendChild(el('p', 'edu-school', P.edu.school));
    eduCard.appendChild(el('p', 'edu-major', P.edu.major + ' · ' + P.edu.degree));
    eduCard.appendChild(el('p', 'edu-period', P.edu.period));
  }

  document.querySelectorAll('.ability-group').forEach(function(n) { n.classList.add('is-visible'); });
  // Contact - 左栏：文字联系方式
  // Contact - 右栏：微信二维码
  var strip = document.getElementById('contact-strip');
  if (strip) {
    // 创建左栏容器
    var contactLeft = el('div', 'contact-left');
    [['电话', P.phone, 'tel:+8615680635573'],
     ['邮箱', P.email, 'mailto:Yangtsegg@163.com'],
     ['所在地', P.location + '（可驻场 / 高频出差）', null],
     ['求职意向', P.target, null]].forEach(function (row) {
      var card = el('a', 'contact-card');
      if (row[2]) card.href = row[2]; else card.href = '#top';
      card.appendChild(el('span', 'c-label', row[0]));
      card.appendChild(el('span', 'c-value', row[1]));
      // 电话和邮箱点击复制
      if (row[2] && row[2].indexOf('tel:') === 0) {
        card.href = 'javascript:void(0)';
        card.addEventListener('click', function(e) { e.preventDefault(); copyToClipboard(P.phone, row[0]); });
      } else if (row[2] && row[2].indexOf('mailto:') === 0) {
        card.href = 'javascript:void(0)';
        card.addEventListener('click', function(e) { e.preventDefault(); copyToClipboard(P.email, row[0]); });
      }
      contactLeft.appendChild(card);
    });
    strip.appendChild(contactLeft);

    // 创建右栏容器 - 微信二维码
    var contactRight = el('div', 'contact-right');
    var qrWrap = el('div', 'qr-wrap');
    var qrImg = el('img', 'qr-img');
    qrImg.setAttribute('src', 'assets/微信二维码截图.png');
    qrImg.setAttribute('alt', '微信二维码');
    qrWrap.appendChild(qrImg);
    var qrLabel = el('p', 'qr-label', '微信扫码添加');
    contactRight.appendChild(qrWrap);
    contactRight.appendChild(qrLabel);
    strip.appendChild(contactRight);
  }
// 复制功能
function showToast(msg) {
  var container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    container.className = "toast-container";
    document.body.appendChild(container);
  }
  var toast = document.createElement("div");
  toast.className = "toast";
  toast.innerHTML = "<span class=\"toast-icon\">\u2713</span>" + msg;
  container.appendChild(toast);
  requestAnimationFrame(function() { toast.classList.add("show"); });
  setTimeout(function() {
    toast.classList.remove("show");
    setTimeout(function() { container.removeChild(toast); }, 300);
  }, 2000);
}

function copyToClipboard(text, label) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(function() {
      showToast(label + " 已复制到剪贴板");
    }).catch(function() {
      fallbackCopy(text, label);
    });
  } else {
    fallbackCopy(text, label);
  }
}

function fallbackCopy(text, label) {
  var ta = document.createElement("textarea");
  ta.value = text;
  ta.style.position = "fixed"; ta.style.left = "-9999px";
  document.body.appendChild(ta); ta.select();
  try { document.execCommand("copy"); showToast(label + " 已复制到剪贴板"); }
  catch(e) { showToast("复制失败，请手动复制"); }
  document.body.removeChild(ta);
}
})();
