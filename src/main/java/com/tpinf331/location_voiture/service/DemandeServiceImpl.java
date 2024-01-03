package com.tpinf331.location_voiture.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.tpinf331.location_voiture.modele.Demande;
import com.tpinf331.location_voiture.repository.DemandeRepository;

import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class DemandeServiceImpl implements DemandeService {
    
    private final DemandeRepository demandeRepository;

    @Override
    public Demande creer(Demande demande){
        return demandeRepository.save(demande);
    }

    @Override
    public List<Demande> lire(){
        return demandeRepository.findAll();
    }

    @Override
    public Demande modifier(int idDemande , Demande demande){
        return demandeRepository.findById(idDemande)
            .map(d->{
                d.setNom(demande.getNom());
                d.setPrenom(demande.getPrenom());
                d.setEmail(demande.getEmail());
                d.setNumeroCNI(demande.getNumeroCNI());
                d.setDateNaissance(demande.getDateNaissance());
                d.setVille(demande.getVille());
                d.setNombreVoiture(demande.getNombreVoiture());
                return demandeRepository.save(d);
            }).orElseThrow(()-> new RuntimeException("demande pas trouve !"));
    }

    @Override
    public String supprimer(int idDemande){
        demandeRepository.deleteById(idDemande);
        return "demande supprime !";
    }
}
