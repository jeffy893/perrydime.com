/**
 * Perry Dime Website - Main JavaScript
 * Handles mobile navigation and interactive features
 */

(function() {
    'use strict';
    
    // ========================================
    // Mobile Menu Toggle
    // ========================================
    
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuToggle && navLinks) {
        mobileMenuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            
            // Animate hamburger icon
            const spans = this.querySelectorAll('span');
            if (navLinks.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
        
        // Close mobile menu when clicking a link
        const navLinkItems = navLinks.querySelectorAll('a');
        navLinkItems.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    navLinks.classList.remove('active');
                    const spans = mobileMenuToggle.querySelectorAll('span');
                    spans[0].style.transform = 'none';
                    spans[1].style.opacity = '1';
                    spans[2].style.transform = 'none';
                }
            });
        });
    }
    
    // ========================================
    // Smooth Scroll for Anchor Links
    // ========================================
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // ========================================
    // Header Scroll Effect
    // ========================================
    
    const header = document.querySelector('.site-header');
    let lastScroll = 0;
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        // Add shadow when scrolled
        if (currentScroll > 10) {
            header.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
        } else {
            header.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
        }
        
        lastScroll = currentScroll;
    });
    
    // ========================================
    // Set Active Navigation Link
    // ========================================
    
    function setActiveNavLink() {
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        const navLinkItems = document.querySelectorAll('.nav-links a');
        
        navLinkItems.forEach(link => {
            link.classList.remove('active');
            const linkPage = link.getAttribute('href');
            if (linkPage === currentPage || (currentPage === '' && linkPage === 'index.html')) {
                link.classList.add('active');
            }
        });
    }
    
    // Set active link on page load
    setActiveNavLink();
    
    // ========================================
    // Image Lazy Loading (for future use)
    // ========================================
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        observer.unobserve(img);
                    }
                }
            });
        });
        
        // Observe all images with data-src attribute
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // ========================================
    // Console Message
    // ========================================
    
    console.log('%cPerry Dime', 'font-size: 24px; font-weight: bold; color: #c8af99;');
    console.log('%cPublications, Art, Dreams, and Music', 'font-size: 14px; color: #603e29;');
    
    // ========================================
    // Art Gallery Lightbox
    // ========================================
    
    function initArtGalleryLightbox() {
        const artLinks = document.querySelectorAll('.art-link');
        
        if (artLinks.length === 0) {
            return; // Not on art page
        }
        
        // Create lightbox element
        const lightbox = document.createElement('div');
        lightbox.className = 'lightbox';
        lightbox.innerHTML = `
            <button class="lightbox-close" aria-label="Close lightbox">&times;</button>
            <button class="lightbox-nav lightbox-prev" aria-label="Previous image">&lsaquo;</button>
            <button class="lightbox-nav lightbox-next" aria-label="Next image">&rsaquo;</button>
            <div class="lightbox-content">
                <img src="" alt="">
                <div class="lightbox-title"></div>
            </div>
        `;
        document.body.appendChild(lightbox);
        
        const lightboxImg = lightbox.querySelector('img');
        const lightboxTitle = lightbox.querySelector('.lightbox-title');
        const closeBtn = lightbox.querySelector('.lightbox-close');
        const prevBtn = lightbox.querySelector('.lightbox-prev');
        const nextBtn = lightbox.querySelector('.lightbox-next');
        
        let currentIndex = 0;
        const images = Array.from(artLinks).map(link => ({
            src: link.getAttribute('href'),
            title: link.getAttribute('data-title') || ''
        }));
        
        function showImage(index) {
            currentIndex = index;
            lightboxImg.src = images[index].src;
            lightboxImg.alt = images[index].title;
            lightboxTitle.textContent = images[index].title;
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
        
        function closeLightbox() {
            lightbox.classList.remove('active');
            document.body.style.overflow = '';
        }
        
        function showNext() {
            currentIndex = (currentIndex + 1) % images.length;
            showImage(currentIndex);
        }
        
        function showPrev() {
            currentIndex = (currentIndex - 1 + images.length) % images.length;
            showImage(currentIndex);
        }
        
        // Add click handlers to art links
        artLinks.forEach((link, index) => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                showImage(index);
            });
        });
        
        // Close button
        closeBtn.addEventListener('click', closeLightbox);
        
        // Navigation buttons
        nextBtn.addEventListener('click', showNext);
        prevBtn.addEventListener('click', showPrev);
        
        // Close on background click
        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox) {
                closeLightbox();
            }
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', function(e) {
            if (!lightbox.classList.contains('active')) return;
            
            switch(e.key) {
                case 'Escape':
                    closeLightbox();
                    break;
                case 'ArrowRight':
                    showNext();
                    break;
                case 'ArrowLeft':
                    showPrev();
                    break;
            }
        });
    }
    
    // Initialize lightbox when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initArtGalleryLightbox);
    } else {
        initArtGalleryLightbox();
    }
    
    // ========================================
    // Publications Tab Switching
    // ========================================
    
    function initPublicationTabs() {
        const tabButtons = document.querySelectorAll('.pub-tab');
        const tabContents = document.querySelectorAll('.pub-tab-content');
        
        if (tabButtons.length === 0) {
            return; // Not on publications page
        }
        
        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                const targetTab = this.getAttribute('data-tab');
                
                // Remove active class from all tabs and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Show corresponding content
                const targetContent = document.getElementById(`${targetTab}-content`);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
            });
        });
    }
    
    // Initialize tabs when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPublicationTabs);
    } else {
        initPublicationTabs();
    }
    
    // ========================================
    // Art Gallery Tab Switching
    // ========================================
    
    function initArtTabs() {
        const tabButtons = document.querySelectorAll('.art-tab');
        const tabContents = document.querySelectorAll('.art-tab-content');
        
        if (tabButtons.length === 0) {
            return; // Not on art page
        }
        
        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                const targetTab = this.getAttribute('data-tab');
                
                // Remove active class from all tabs and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Show corresponding content
                const targetContent = document.getElementById(`${targetTab}-content`);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
                
                // Reinitialize lightbox for newly visible images
                initArtGalleryLightbox();
            });
        });
    }
    
    // Initialize art tabs when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initArtTabs);
    } else {
        initArtTabs();
    }
    
    // ========================================
    // Music Tab Switching
    // ========================================
    
    function initMusicTabs() {
        const tabButtons = document.querySelectorAll('.music-tab');
        const tabContents = document.querySelectorAll('.music-tab-content');
        
        if (tabButtons.length === 0) {
            return; // Not on music page
        }
        
        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                const targetTab = this.getAttribute('data-tab');
                
                // Remove active class from all tabs and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Show corresponding content
                const targetContent = document.getElementById(`${targetTab}-content`);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
            });
        });
    }
    
    // Initialize music tabs when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMusicTabs);
    } else {
        initMusicTabs();
    }
    
})();
