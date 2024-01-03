package com.tpinf331.location_voiture.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.tpinf331.location_voiture.modele.Voiture;
import com.tpinf331.location_voiture.repository.VoitureRepository;

import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class VoitureServiceImpl implements VoitureService {

    private final VoitureRepository voitureRepository;


    @Override
    public Voiture creer(Voiture voiture){
        return voitureRepository.save(voiture);
    }

    @Override
    public List<Voiture> lire(){
        return voitureRepository.findAll();
    }

    @Override
        public Voiture modifier(int idVoiture , Voiture voiture){
        return voitureRepository.findById(idVoiture)
            .map(v->{
                v.setMarque(voiture.getMarque());
                v.setVersion(voiture.getVersion());
                v.setAnneeFabrication(voiture.getAnneeFabrication());
                return voitureRepository.save(v);
            }).orElseThrow(()-> new RuntimeException("voiture non trouve"));
    }

    @Override
    public String supprimer(int idVoiture){
        voitureRepository.deleteById(idVoiture);
        return "voiture supprime" ;
    }
}
