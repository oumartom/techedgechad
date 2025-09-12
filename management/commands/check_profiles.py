from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from techEdgeApp.models import UserProfile

class Command(BaseCommand):
    help = 'Vérifie et corrige les profils utilisateur'
    
    def handle(self, *args, **options):
        # 1. Vérifier tous les utilisateurs
        users = User.objects.all()
        self.stdout.write(f"Nombre total d'utilisateurs: {users.count()}")
        
        # 2. Vérifier les profils manquants
        users_without_profile = []
        for user in users:
            try:
                profile = user.profile
            except UserProfile.DoesNotExist:
                users_without_profile.append(user)
                # Créer le profil manquant
                UserProfile.objects.create(user=user)
                self.stdout.write(f"✅ Profil créé pour: {user.username}")
        
        if users_without_profile:
            self.stdout.write(f"\n🔧 {len(users_without_profile)} profils créés")
        else:
            self.stdout.write("\n✅ Tous les utilisateurs ont un profil")
        
        # 3. Afficher tous les profils avec leur téléphone
        self.stdout.write("\n📋 Liste des profils et téléphones:")
        self.stdout.write("-" * 50)
        for profile in UserProfile.objects.all().select_related('user'):
            phone_display = profile.phone if profile.phone else "❌ Non renseigné"
            self.stdout.write(f"{profile.user.username:20} | {phone_display}")