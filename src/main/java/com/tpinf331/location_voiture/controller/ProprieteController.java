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

import com.tpinf331.location_voiture.modele.Propriete;
import com.tpinf331.location_voiture.service.ProprieteService;

import lombok.AllArgsConstructor;



@RestController
@RequestMapping("/propriete")
@AllArgsConstructor
public class ProprieteController {
    
    private final ProprieteService proprieteService;

    @PostMapping("/create")
    public Propriete create(@RequestBody Propriete propriete){
        return proprieteService.creer(propriete);
    }

    @GetMapping("/read")
    public List<Propriete> read(){
        return proprieteService.lire();
    }

    @PutMapping("/update/{idPropriete}")
    public Propriete update(@PathVariable int idPropriete , @RequestBody Propriete propriete){
        return proprieteService.modifier(idPropriete, propriete);
    }

    @DeleteMapping("/delete/{idPropriete}")
    public String delete(@PathVariable int idPropriete){
        return proprieteService.supprimer(idPropriete);
    }
}
