const loadArticle = (pathAndHash, articleElement, headerElement, breadcrumbsElement) => {
    console.log(`Loading article '${pathAndHash}'`);
    const
        hashIndex = pathAndHash.indexOf('#'),
        path = hashIndex >= 0 ? pathAndHash.substring(0, hashIndex) : pathAndHash,
        hash = hashIndex >= 0 ? pathAndHash.substring(pathAndHash.indexOf('#') + 1) : undefined;
    fetch(path || 'index')
        .then(res => res.text())
        .then(text => {
            const root = document.createElement('div');
            root.innerHTML = text;
            headerElement.innerHTML = (root.querySelector('header') || {innerHTML: ''}).innerHTML;
            articleElement.innerHTML = (root.querySelector('article') || {innerHTML: ''}).innerHTML;
            document.title = `${headerElement.innerHTML} - alcrea.info`;
            let dir = path.substring(0, path.lastIndexOf('/'));
            articleElement.querySelectorAll('a[href]').forEach(a => {
                let href = a.getAttribute('href');
                if (href[0] !== '/') href = `${dir}/${href}`;
                a.setAttribute('href', href === 'index.md' ? '#' : `#${href}`);
            });
            breadcrumbsElement.innerHTML = ' /';
            while(dir) {
                const breadcrumb = document.createElement('a');
                breadcrumb.href = `#${dir}/`;
                breadcrumb.innerText = dir.substring(dir.lastIndexOf('/') + 1);
                breadcrumbsElement.innerHTML = ' / ' + breadcrumb.outerHTML + breadcrumbsElement.innerHTML;
                dir = dir.substring(0, dir.lastIndexOf('/'));
            }
            const breadcrumb = document.createElement('a');
            breadcrumb.href = `#`;
            breadcrumb.innerText = 'alcrea.info';
            breadcrumbsElement.innerHTML = ' / ' + breadcrumb.outerHTML + breadcrumbsElement.innerHTML;
            if (hash) {
                const anchor = articleElement.querySelector(`a[name="${hash}"]`);
                if (anchor) anchor.scrollIntoView()
            }

        });
};

window.onload = () => {
    const
        articleElement = document.querySelector('article'),
        headerElement = document.querySelector('header'),
        breadcrumbsElement = document.querySelector('div.breadcrumbs'),
        hash = window.location.hash.substring(1) || '';
    window.onpopstate = e => loadArticle(
        window.location.hash.substring(1),
        articleElement,
        headerElement,
        breadcrumbsElement
    );
    document.onkeydown = e => {
        if (e.ctrlKey && e.altKey && e.key === 'r') loadArticle(
            window.location.hash.substring(1),
            articleElement,
            headerElement,
            breadcrumbsElement
        );
    };
    history.replaceState({hash: hash}, document.title);
    loadArticle(hash, articleElement, headerElement, breadcrumbsElement);

};
