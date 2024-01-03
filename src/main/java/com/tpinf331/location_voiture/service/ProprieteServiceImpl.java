package com.tpinf331.location_voiture.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.tpinf331.location_voiture.modele.Propriete;
import com.tpinf331.location_voiture.repository.ProprieteRepository;

import lombok.AllArgsConstructor;


@Service
@AllArgsConstructor
public class ProprieteServiceImpl implements ProprieteService {
    
    private final ProprieteRepository proprieteRepository;

    @Override
    public Propriete creer(Propriete propriete){
        return proprieteRepository.save(propriete);
    }

    @Override
    public List<Propriete> lire(){
        return proprieteRepository.findAll();
    }

    @Override
    public Propriete modifier(int idPropriete , Propriete propriete){
        return proprieteRepository.findById(idPropriete)
            .map(p->{
                p.setPrix(propriete.getPrix());
                p.setVitesse(propriete.getVitesse());
                p.setTypeCarburant(propriete.getTypeCarburant());
                p.setTypeMoteur(propriete.getTypeMoteur());
                p.setPuissance(propriete.getPuissance());
                p.setCouleur(propriete.getCouleur());
                return proprieteRepository.save(p);
            }).orElseThrow(()-> new RuntimeException("propriete pas trouve !"));
    }
    @Override
    public String supprimer(int idPropriete){
        proprieteRepository.deleteById(idPropriete);
        return "propriete supprime !";
    }
}
