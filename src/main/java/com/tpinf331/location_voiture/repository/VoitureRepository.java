package com.tpinf331.location_voiture.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.tpinf331.location_voiture.modele.Voiture;

public interface VoitureRepository extends JpaRepository<Voiture , Integer> {
    
    
}
