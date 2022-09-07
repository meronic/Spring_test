package com.example.firstApplication.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class FirstController {

    @GetMapping("/hi")
    public String niceToMeetYou(Model model){
        model.addAttribute("username", "Meronic");
        return "greetings"; // templates/greetings.mustache
    }

    @GetMapping("/bye")
    public String goodBye(Model model){
        model.addAttribute("username", "Meronic");
        return "goodbye";
    }
}
