package com.tpinf331.location_voiture.service;

import java.util.List;
import com.tpinf331.location_voiture.modele.User;

public interface UserService {
    
    User creer(User user);

    List<User> lire();

    User modifier(int id , User user);

    String supprimer(int id);
}
