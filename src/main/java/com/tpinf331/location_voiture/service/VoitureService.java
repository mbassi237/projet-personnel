package com.tpinf331.location_voiture.service;

import java.util.List;
import com.tpinf331.location_voiture.modele.Voiture;

public interface VoitureService {
    
    Voiture creer(Voiture voiture);

    List<Voiture> lire();

    Voiture modifier(int idVoiture , Voiture voiture);

    String supprimer(int idVoiture);
}
