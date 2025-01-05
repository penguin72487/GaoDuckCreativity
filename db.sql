create table team_files (
    id serial primary key,
    team_id integer not null,
    file_path varchar(255) not null,
    foreign key (team_id) references teams (id),
);

create table announcement_files (
    id serial primary key,
    announcement_id integer not null,
    file_path varchar(255) not null,
    foreign key (announcement_id) references announcements (id),
);

create table team_members(
    primary key (u_id, t_id),
);
