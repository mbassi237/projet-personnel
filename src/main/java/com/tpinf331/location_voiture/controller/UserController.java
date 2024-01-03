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

import com.tpinf331.location_voiture.modele.User;
import com.tpinf331.location_voiture.service.UserService;

import lombok.AllArgsConstructor;

@RestController
@RequestMapping("/user")
@AllArgsConstructor
public class UserController {
    
    private final UserService userService;

    @PostMapping("/create")
    public User create(@RequestBody User user){
        return userService.creer(user);
    }

    @GetMapping("/read")
    public List<User> read(){
        return userService.lire();
    }

    @PutMapping("/update/{id}")
    public User update(@PathVariable int id , @RequestBody User user){
        return userService.modifier(id, user);
    }

    @DeleteMapping("/delete/{id}")
    public String delete(@PathVariable int id){
        return userService.supprimer(id);
    }

}
