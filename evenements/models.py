from django.conf import settings
from django.db import models

from core.models import SyncableModel


class Evenement(SyncableModel):
    TYPE_CHOICES = [
        ("messe", "Messe"),
        ("fete_liturgique", "Fête liturgique"),
        ("reunion", "Réunion"),
        ("kermesse", "Kermesse"),
        ("reservation", "Réservation"),
    ]

    titre = models.CharField(max_length=255)
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
    )
    description = models.TextField(blank=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField(null=True, blank=True)
    lieu = models.CharField(max_length=255, blank=True)
    est_inscription_requise = models.BooleanField(default=False)
    createur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="evenements_crees",
    )

    # --- Conviés (convocations) ------------------------------------------------
    # Un événement peut convier selon 4 axes cumulables. Un utilisateur est
    # convié si : invite_tous, OU son rôle ∈ roles_invites, OU sa fiche membre
    # appartient à un groupe de groupes_invites, OU sa fiche ∈ membres_invites.
    invite_tous = models.BooleanField(
        default=False, verbose_name="Convier toute la paroisse"
    )
    # Liste de codes de rôle (accounts.User.ROLES_CHOICES), ex: ["fidele", "pretre"].
    roles_invites = models.JSONField(default=list, blank=True)
    groupes_invites = models.ManyToManyField(
        "groupes.Groupe", blank=True, related_name="evenements_invites"
    )
    membres_invites = models.ManyToManyField(
        "membres.Membre", blank=True, related_name="evenements_invites"
    )

    @property
    def est_passe(self):
        """Vrai si l'événement est terminé (date_fin si présente, sinon
        date_debut, dépassée)."""
        from django.utils import timezone

        reference = self.date_fin or self.date_debut
        return bool(reference and reference < timezone.now())

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ["-date_debut"]
        indexes = [
            models.Index(fields=["type"], name="evenement_type_idx"),
            models.Index(fields=["date_debut"], name="evenement_date_debut_idx"),
        ]

    def __str__(self):
        return self.titre


class Participation(SyncableModel):
    evenement = models.ForeignKey(
        Evenement, on_delete=models.CASCADE, related_name="participations"
    )
    membre = models.ForeignKey(
        "membres.Membre", on_delete=models.CASCADE, related_name="participations"
    )
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Participation"
        verbose_name_plural = "Participations"
        unique_together = ("evenement", "membre")

    def __str__(self):
        return f"{self.membre} → {self.evenement}"
