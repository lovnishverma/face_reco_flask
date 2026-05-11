/**
 * FaceVault — Frontend Interactivity
 * Drag-and-drop, image preview, mobile nav, flash auto-dismiss
 */

document.addEventListener('DOMContentLoaded', () => {

    // ─── Mobile Sidebar Toggle ───
    const toggle = document.getElementById('mobile-toggle');
    const sidebar = document.getElementById('sidebar');
    if (toggle && sidebar) {
        toggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
        // Close on outside click
        document.addEventListener('click', (e) => {
            if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && !toggle.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        });
    }

    // ─── Drag and Drop Upload ───
    const uploadZone = document.getElementById('upload-zone');
    const uploadInput = document.getElementById('photo');
    const uploadContent = document.getElementById('upload-content');
    const uploadPreview = document.getElementById('upload-preview');
    const previewImage = document.getElementById('preview-image');
    const previewRemove = document.getElementById('preview-remove');

    if (uploadZone && uploadInput) {
        // Drag events
        ['dragenter', 'dragover'].forEach(event => {
            uploadZone.addEventListener(event, (e) => {
                e.preventDefault();
                uploadZone.classList.add('drag-over');
            });
        });

        ['dragleave', 'drop'].forEach(event => {
            uploadZone.addEventListener(event, (e) => {
                e.preventDefault();
                uploadZone.classList.remove('drag-over');
            });
        });

        uploadZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                uploadInput.files = files;
                showPreview(files[0]);
            }
        });

        // File input change
        uploadInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                showPreview(e.target.files[0]);
            }
        });

        // Remove preview
        if (previewRemove) {
            previewRemove.addEventListener('click', (e) => {
                e.stopPropagation();
                uploadInput.value = '';
                hidePreview();
            });
        }
    }

    function showPreview(file) {
        if (!file.type.startsWith('image/')) return;
        const reader = new FileReader();
        reader.onload = (e) => {
            if (previewImage) previewImage.src = e.target.result;
            if (uploadContent) uploadContent.style.display = 'none';
            if (uploadPreview) uploadPreview.style.display = 'flex';
        };
        reader.readAsDataURL(file);
    }

    function hidePreview() {
        if (uploadContent) uploadContent.style.display = 'flex';
        if (uploadPreview) uploadPreview.style.display = 'none';
        if (previewImage) previewImage.src = '';
    }

    // ─── Auto-dismiss Flash Messages ───
    document.querySelectorAll('.flash-message').forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            setTimeout(() => msg.remove(), 300);
        }, 5000);
    });

    // ─── Animate Stats on Scroll ───
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.stat-card, .action-card, .result-card, .person-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });
});
