package com.tpinf331.location_voiture.service;

import java.util.List;

import com.tpinf331.location_voiture.modele.Demande;

public interface DemandeService {
    
    Demande creer(Demande demande);

    List<Demande> lire();

    Demande modifier(int idDemande , Demande demande);

    String supprimer(int idDemande);
}
