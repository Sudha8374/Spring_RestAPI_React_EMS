package com.sample.springboot;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.sample.springboot.model.User;
import com.sample.springboot.repository.UserRepository;

@SpringBootApplication
public class SpringbootBackendApplication implements CommandLineRunner{
	

	public static void main(String[] args) {
		SpringApplication.run(SpringbootBackendApplication.class, args);
	}
    @Autowired
    private UserRepository userRepository;
    
	@Override
	public void run(String... args) throws Exception {
	   this.userRepository.save(new User("om","sudha","sudha@gmail.com"));
	   this.userRepository.save(new User("sree","mani","sree@gmail.com"));
	   this.userRepository.save(new User("Tony","stark","tony@gmail.com"));
	}

}
