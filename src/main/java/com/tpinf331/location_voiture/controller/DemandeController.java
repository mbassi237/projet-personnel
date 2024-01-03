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

import com.tpinf331.location_voiture.modele.Demande;
import com.tpinf331.location_voiture.service.DemandeService;

import lombok.AllArgsConstructor;

@RestController
@RequestMapping("/demande")
@AllArgsConstructor
public class DemandeController {
    
    private final DemandeService demandeService;

    @PostMapping("/create")
    public Demande create(@RequestBody Demande demande){
        return demandeService.creer(demande);
    }

    @GetMapping("/read")
    public List<Demande> read(){
        return demandeService.lire();
    }

    @PutMapping("/update/{idDemande}")
    public Demande update(@PathVariable int idDemande , @RequestBody Demande demande){
        return demandeService.modifier(idDemande, demande);
    }

    @DeleteMapping("/delete/{idDemande}")
    public String delete(@PathVariable int idDemande){
        return demandeService.supprimer(idDemande);
    }
}
