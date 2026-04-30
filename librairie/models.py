from django.conf import settings
from django.db import models


class Article(models.Model):
    CATEGORIE_CHOICES = [
        ("livre", "Livre"),
        ("bougie", "Bougie"),
        ("chapelet", "Chapelet"),
        ("vetement", "Vêtement"),
        ("autre", "Autre"),
    ]

    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    stock_disponible = models.PositiveIntegerField(default=0)
    seuil_alerte = models.PositiveIntegerField(default=5)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ["nom"]

    def __str__(self):
        return self.nom

    @property
    def en_alerte(self):
        return self.stock_disponible <= self.seuil_alerte


class Vente(models.Model):
    article = models.ForeignKey(Article, on_delete=models.PROTECT, related_name="ventes")
    quantite = models.PositiveIntegerField()
    prix_total = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    membre = models.ForeignKey(
        "membres.Membre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="achats",
    )
    enregistre_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ventes_enregistrees",
    )

    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.article} × {self.quantite} ({self.date:%d/%m/%Y})"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.prix_total = self.article.prix_unitaire * self.quantite
            self.article.stock_disponible -= self.quantite
            self.article.save()
        super().save(*args, **kwargs)
