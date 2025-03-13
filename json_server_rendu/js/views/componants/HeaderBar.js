export default class Headerbar {
    static async render() {
        return `
        <nav class="navbar navbar-expand-lg bg-primary" data-bs-theme="dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#/">LAW AND ORDER</a>
            <div class="collapse navbar-collapse" id="navbarColor01">
            <ul class="navbar-nav me-auto">
                <li class="nav-item">
                <a class="nav-link" href="#/articles">Articles</a>
                </li>
                <li class="nav-item">
                <a class="nav-link" href="#/about">About</a>
                </li>
            </ul>
            </div>
        </div>
        </nav>
        `;
    }
} 