package com.tpinf331.location_voiture.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.tpinf331.location_voiture.modele.User;
import com.tpinf331.location_voiture.repository.UserRepository;

import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class UserServiceImpl implements UserService {
    private final UserRepository userRepository;

    @Override
    public User creer(User user){
        return userRepository.save(user);
    }

    @Override
    public List<User> lire(){
        return userRepository.findAll();
    }

    @Override
    public User modifier(int id , User user){
        return userRepository.findById(id)
            .map(u->{
                u.setNom(user.getNom());
                u.setEmail(user.getEmail());
                return userRepository.save(u);
            }).orElseThrow(()-> new RuntimeException("utilisateur non trouve !"));
    }

    @Override
    public String supprimer(int id){
        userRepository.deleteById(id);
        return "utilisateur supprime";
    }
}
