from flask import request, abort
from CTFd.utils.user import get_current_user
from CTFd.plugins import register_plugin_assets_directory

MODERATOR_IDS = [8]

def load(app):
    print(" [CTFd Moderator Plugin] Loaded. Restricted IDs: " + str(MODERATOR_IDS))

    def is_moderator():
        user = get_current_user()
        if user and user.type == 'admin' and user.id in MODERATOR_IDS:
            return True
        return False


    @app.before_request
    def restrict_moderator_actions():
        if not is_moderator():
            return

        path = request.path
        method = request.method


        if path.startswith('/admin/config') or path.startswith('/api/v1/configs'):
            abort(403)


        if path.startswith('/admin/pages') or path.startswith('/api/v1/pages'):
            abort(403)


        if path.startswith('/admin/scoreboard'):
            abort(403)


        if path == '/admin/submissions' or (path == '/api/v1/submissions' and method == 'GET'):
            abort(403)

        if path.startswith('/api/v1/challenges') and method in ['POST', 'PATCH', 'DELETE']:
            abort(403)


    @app.after_request
    def remove_admin_ui_elements(response):
        if not is_moderator():
            return response


        if request.path.startswith('/admin') and response.content_type == 'text/html; charset=utf-8':
            

            js_cleaner = b"""
            <script>
            document.addEventListener("DOMContentLoaded", function() {
                console.log("Moderator Mode: Cleaning UI...");

                // 1. Supprimer les liens du menu de navigation (Sidebar ou Topbar)
                const forbiddenKeywords = ['config', 'pages', 'scoreboard', 'submissions'];
                document.querySelectorAll('.nav-link, .dropdown-item').forEach(link => {
                    const href = link.getAttribute('href');
                    if (href) {
                        forbiddenKeywords.forEach(word => {
                            if (href.includes('/admin/' + word)) {
                                // Cache le li parent ou le lien lui-même
                                if(link.parentElement.tagName === 'LI') link.parentElement.remove();
                                else link.remove();
                            }
                        });
                    }
                });

                // 2. Supprimer le bouton "New Challenge" (souvent id="create-challenge")
                const createBtn = document.getElementById('create-challenge');
                if(createBtn) createBtn.remove();
                
                // 3. Supprimer les boutons d'édition dans la vue challenge
                // (Sélecteur générique pour AdminLTE / CTFd Themes)
                document.querySelectorAll('.fa-pencil-alt, .fa-trash-alt').forEach(icon => {
                    // Vérification contextuelle pour ne pas supprimer les boutons de notifs
                    // Ceci est une approche brutale, à affiner selon votre thème exact
                });
                
                // Cacher les sections d'édition spécifiques aux challenges
                const updateBtn = document.getElementById('challenge-update-button');
                if(updateBtn) updateBtn.remove();
                
                const deleteBtn = document.getElementById('challenge-delete-button');
                if(deleteBtn) deleteBtn.remove();
            });
            </script>
            <style>
                /* Sécurité visuelle CSS supplémentaire */
                a[href*="/admin/config"], 
                a[href*="/admin/pages"],
                a[href*="/admin/scoreboard"],
                a[href*="/admin/submissions"] { display: none !important; }
                
                #create-challenge { display: none !important; }
            </style>
            """
            

            response.data = response.data.replace(b'</body>', js_cleaner + b'</body>')
            
        return response
