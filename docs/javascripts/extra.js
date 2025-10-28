document.addEventListener('DOMContentLoaded', function () {
    const structuredData = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "BlockNote-py",
        "description": "Python library for BlockNote.js - Convert BlockNote blocks to HTML, Markdown, and JSON with full type safety",
        "url": "https://rohansharmasitoula.github.io/blocknote-py/",
        "downloadUrl": "https://pypi.org/project/blocknote-py/",
        "author": {
            "@type": "Person",
            "name": "Rohan Sharma Sitoula",
            "url": "https://github.com/rohansharmasitoula"
        },
        "programmingLanguage": "Python",
        "operatingSystem": "Cross-platform",
        "applicationCategory": "DeveloperApplication",
        "keywords": [
            "blocknote",
            "python",
            "blocknote-py",
            "blocknote python",
            "block note python",
            "html converter",
            "markdown converter",
            "json converter",
            "blocknotejs",
            "rich text editor",
            "content management"
        ],
        "license": "https://opensource.org/licenses/MIT",
        "codeRepository": "https://github.com/rohansharmasitoula/blocknote-py"
    };

    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(structuredData);
    document.head.appendChild(script);

    const metaTags = [
        { property: 'og:title', content: 'BlockNote-py - Python Library for BlockNote.js' },
        { property: 'og:description', content: 'Convert BlockNote blocks to HTML, Markdown, and JSON with Python. Full type safety and validation.' },
        { property: 'og:type', content: 'website' },
        { property: 'og:url', content: 'https://rohansharmasitoula.github.io/blocknote-py/' },
        { property: 'og:image', content: 'https://rohansharmasitoula.github.io/blocknote-py/assets/og-image.png' },
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: 'BlockNote-py - Python Library for BlockNote.js' },
        { name: 'twitter:description', content: 'Convert BlockNote blocks to HTML, Markdown, and JSON with Python' },
        { name: 'robots', content: 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1' },
        {
            name: 'keywords',
            content: 'blocknote python, blocknote py, blocknote js python, blocknote converter, blocknote-py package, block note python library'
        },
        { property: 'og:site_name', content: 'BlockNote-py' }
    ];

    metaTags.forEach(tag => {
        const meta = document.createElement('meta');
        if (tag.property) {
            meta.setAttribute('property', tag.property);
        } else {
            meta.setAttribute('name', tag.name);
        }
        meta.setAttribute('content', tag.content);
        document.head.appendChild(meta);
    });

    const preloadLinks = [
        { href: '/blocknote-py/assets/stylesheets/main.css', as: 'style' },
        { href: '/blocknote-py/assets/javascripts/bundle.js', as: 'script' }
    ];

    preloadLinks.forEach(link => {
        const preload = document.createElement('link');
        preload.rel = 'preload';
        preload.href = link.href;
        preload.as = link.as;
        document.head.appendChild(preload);
    });

    const canonical = document.createElement('link');
    canonical.rel = 'canonical';
    canonical.href = window.location.origin + window.location.pathname;
    document.head.appendChild(canonical);

    const searchInput = document.querySelector('.md-search__input');
    if (searchInput) {
        searchInput.addEventListener('input', function (e) {
            const query = e.target.value;
            if (query.length > 2) {
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'search', {
                        search_term: query
                    });
                }
            }
        });
    }
});

window.addEventListener('load', function () {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'page_view', {
            page_title: document.title,
            page_location: window.location.href
        });
    }
});
