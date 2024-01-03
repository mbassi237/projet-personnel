package com.tpinf331.location_voiture.modele;

import java.sql.Date;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;


@Entity
@Table(name = "DEMANDE")
@NoArgsConstructor
@Getter
@Setter
public class Demande {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int idDemande;
    private String nom;
    private String prenom;
    private String email;
    private String numeroCNI;
    private Date dateNaissance;
    private String ville;
    private int nombreVoiture;
}
