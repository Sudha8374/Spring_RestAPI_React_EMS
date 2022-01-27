package com.sample.springboot.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.sample.springboot.model.User;
@Repository
public interface UserRepository extends JpaRepository<User,Long> {

}
