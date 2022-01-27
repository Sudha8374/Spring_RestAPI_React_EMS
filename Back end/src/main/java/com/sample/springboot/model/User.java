package com.sample.springboot.model;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name="users")
public class User {
	
@Id
@GeneratedValue(strategy=GenerationType.IDENTITY)

private long id;

@Column(name="first_Name")
private String first_Name;

@Column(name="last_Name")
private String last_Name;
private String email;


public User()
{
  	
}
public User(String first_Name, String last_Name, String email) {
	super();
	this.first_Name = first_Name;
	this.last_Name = last_Name;
	this.email = email;
}
public long getId() {
	return id;
}
public void setId(long id) {
	this.id = id;
}
public String getFirst_Name() {
	return first_Name;
}
public void setFirst_Name(String first_Name) {
	this.first_Name = first_Name;
}
public String getLast_Name() {
	return last_Name;
}
public void setLastName(String last_Name) {
	this.last_Name = last_Name;
}
public String getEmail() {
	return email;
}
public void setEmail(String email) {
	this.email = email;
}

}
