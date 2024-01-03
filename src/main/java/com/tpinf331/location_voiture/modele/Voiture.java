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
@Table(name ="VOITURE")
@NoArgsConstructor
@Getter
@Setter
public class Voiture {
    

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int idVoiture;
    private String marque;
    private Date anneeFabrication;
    private String version;
}
