package com.tpinf331.location_voiture.controller;

import java.util.List;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.tpinf331.location_voiture.modele.Voiture;
import com.tpinf331.location_voiture.service.VoitureService;

import lombok.AllArgsConstructor;

@RestController
@RequestMapping("/voiture")
@AllArgsConstructor
public class VoitureController {
    
    private final VoitureService voitureService;

    @PostMapping("/create")
    public Voiture create(@RequestBody Voiture voiture){
        return voitureService.creer(voiture);
    }

    @GetMapping("/read")
    public List<Voiture> read(){
        return voitureService.lire();
    }

    @PutMapping("/update/{idVoiture}")
    public Voiture update(@PathVariable int idVoiture , @RequestBody Voiture voiture){
        return voitureService.modifier(idVoiture, voiture);
    }

    @DeleteMapping("/delete/{idVoiture}")
    public String delete(@PathVariable int idVoiture){
        return voitureService.supprimer(idVoiture);
    }

}
