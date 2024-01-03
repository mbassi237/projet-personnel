package com.tpinf331.location_voiture.modele;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "PROPRIETE")
@NoArgsConstructor
@Getter
@Setter
public class Propriete {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int idPropriete;
    private int prix;
    private float vitesse;
    private String typeCarburant;
    private String typeMoteur;
    private String puissance;
    private String couleur;
}
