document.addEventListener('DOMContentLoaded', () => {
    // 1. Fade-in animation for cards
    const cards = document.querySelectorAll('.gitspec-card');
    
    // Add initial opacity 0 if there are cards
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    });

    // Use IntersectionObserver to animate when scrolled into view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    cards.forEach(card => observer.observe(card));

    // 2. Open GitHub links in a new tab
    const externalLinks = document.querySelectorAll('a[href^="http"]');
    externalLinks.forEach(link => {
        if (!link.hasAttribute('target')) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });

    // 3. Fetch GitHub metrics dynamically for elements with data-repo
    const metricsElements = document.querySelectorAll('[data-repo]');
    metricsElements.forEach(async (el) => {
        const repo = el.getAttribute('data-repo');
        try {
            const response = await fetch(`/api/github/${repo}`);
            if (response.ok) {
                const data = await response.json();
                
                // Update stars
                const starsEl = el.querySelector('.github-stars');
                if (starsEl && data.stars !== undefined) {
                    starsEl.innerHTML = `⭐ ${data.stars}`;
                }

                // Update language
                const langEl = el.querySelector('.github-lang');
                if (langEl && data.language) {
                    langEl.innerHTML = `🔵 ${data.language}`;
                }
            }
        } catch (error) {
            console.error('Error fetching github metrics for', repo, error);
        }
    });
});
