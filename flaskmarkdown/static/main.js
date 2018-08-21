function extractArticleAndHeader(text) {
    const root = document.createElement('div');
    root.innerHTML = text;
    const
        articleElement = root.querySelector('article'),
        headerElement = (root.querySelector('header') || {innerHTML: ''});
    if (!articleElement || articleElement.innerHTML === undefined) throw 'No article tag in document';
    return {articleHtml: articleElement.innerHTML, headerHtml: headerElement.innerHTML};
}

function fixAnchorHrefsInElement(element, dir) {
    element.querySelectorAll('a[href]').forEach(a => {
        let href = a.getAttribute('href');
        if (href[0] !== '/') href = `${dir}/${href}`;
        a.setAttribute('href', `#${href}`);
    });
}

function* reverseGenerateBreadcrumbs(dir) {
    while(dir) {
        const breadcrumb = document.createElement('a');
        breadcrumb.href = `#${dir}/`;
        breadcrumb.innerText = dir.substring(dir.lastIndexOf('/') + 1);
        yield breadcrumb;
        dir = dir.substring(0, dir.lastIndexOf('/'));
    }
    const breadcrumb = document.createElement('a');
    breadcrumb.href = `#`;
    breadcrumb.innerText = 'alcrea.info';
    yield breadcrumb;
}

function injectBreadcrumbs(element, dir) {
    element.innerHTML = ' /';
    for(const breadcrumb of reverseGenerateBreadcrumbs(dir)) {
        element.innerHTML = ' / ' + breadcrumb.outerHTML + element.innerHTML;
    }
}

function loadArticle(pathAndHash, articleElement, headerElement, breadcrumbsElement) {
    console.log(`Loading article '${pathAndHash}'`);
    const
        hashIndex = pathAndHash.indexOf('#'),
        path = (hashIndex >= 0 ? pathAndHash.substring(0, hashIndex) : pathAndHash).replace(/\/+$/, '/'),
        hash = hashIndex >= 0 ? pathAndHash.substring(pathAndHash.indexOf('#') + 1) : undefined;
    fetch(path || '/index')
        .then(res => res.text())
        .then(text => {
            const {articleHtml, headerHtml} = extractArticleAndHeader(text);
            articleElement.innerHTML = articleHtml;
            headerElement.innerHTML = headerHtml;
            document.title = `${headerHtml} - alcrea.info`;

            const dir = path.substring(0, path.lastIndexOf('/'));
            fixAnchorHrefsInElement(articleElement, dir);

            injectBreadcrumbs(breadcrumbsElement, dir);

            if (hash) {
                const anchor = articleElement.querySelector(`a[name="${hash}"]`);
                if (anchor) anchor.scrollIntoView()
            }
        });
}

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
