package com.githubpulse.model.entity;

import jakarta.persistence.Entity;

@Entity
public class GitHubEvent {
    public String repoName;
    public String actorLogin;
    public String eventType;
    public String createdAt;
    public String language;
}
