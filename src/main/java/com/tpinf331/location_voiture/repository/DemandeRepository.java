package com.tpinf331.location_voiture.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.tpinf331.location_voiture.modele.Demande;

public interface DemandeRepository extends JpaRepository<Demande , Integer> {
    
}
