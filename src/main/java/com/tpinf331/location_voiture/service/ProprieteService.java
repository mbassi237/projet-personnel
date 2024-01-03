package com.tpinf331.location_voiture.service;

import java.util.List;

import com.tpinf331.location_voiture.modele.Propriete;

public interface ProprieteService {
    
    Propriete creer(Propriete propriete);

    List<Propriete> lire();

    Propriete modifier(int idPropriete , Propriete propriete);

    String supprimer(int idPropriete);
}
