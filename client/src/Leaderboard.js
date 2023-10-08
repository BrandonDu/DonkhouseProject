import React, { useState } from "react";
import { Link, useLoaderData, useNavigate } from "react-router-dom";
import Select from 'react-select';

export default function Leaderboard() {
    const players = useLoaderData()
    // const testtest = JSON.parse(players[0].stats).nets;
    const [selectedOption, setSelectedOption] = useState("hello");
    const [leaderboardOption, setLeaderboardOption] = useState("biggest winners");
    const navigate = useNavigate();

    const handleLeaderboardToggle = (option) => {
        setLeaderboardOption(option);
    };

    const extractPlayers = () => {
      const result = [];

      for (let i = 0; i < players.length; i++) {
        const obj = players[i];
        const username = obj.username;
        const newObj = { value: username, label: username };
        result.push(newObj);
      }
      return result;
    }
    const options = extractPlayers(players);

    const filteredPlayerList = () => {
        if (leaderboardOption === "biggest winners") {
            return players
                .filter((player) => JSON.parse(player.stats).net > 0)
                .sort((a, b) => JSON.parse(b.stats).net - JSON.parse(a.stats).net)
                .slice(0, 10);
        }
        else if (leaderboardOption === "most games played") {
            return players
                .filter((player) => Object.keys(JSON.parse(player.stats).nets).length > 0)
                .sort((a, b) => Object.keys(JSON.parse(b.stats).nets).length - Object.keys(JSON.parse(a.stats).nets).length)
                .slice(0, 10);
        }
        else if (leaderboardOption === "most aggressive") {
          return players
              .filter((player) => JSON.parse(player.stats).vpip[1] > 0)
              .sort((a, b) => JSON.parse(b.stats).vpip[0]/JSON.parse(b.stats).vpip[1]
                 - JSON.parse(a.stats).vpip[0]/JSON.parse(a.stats).vpip[1])
              .slice(0, 15);
        }  
        else if (leaderboardOption === "donk betting board of shame") {
            return players
                .filter((player) => JSON.parse(player.stats).donk[1] > 0)
                .sort((a, b) => JSON.parse(b.stats).donk[0]/JSON.parse(b.stats).donk[1]
                 - JSON.parse(a.stats).donk[0]/JSON.parse(a.stats).donk[1])
                .slice(0, 10);
        } else {
            return players;
        }
    };

    const handleOptionChange = e => {
      setSelectedOption(e.value);
      const link = e.value.toString();
      navigate(link)
    };

    return (
        <div className="board">
          <Select 
            options={options} 
            onChange={handleOptionChange}
            value={options.filter(function(option) {
              return option.value === selectedOption;
            })} 
          />
          <div className="duration">
                <button
                    className={leaderboardOption === "biggest winners" ? "active" : ""}
                    onClick={() => handleLeaderboardToggle("biggest winners")}
                >
                    Winningest
                </button>
                <button
                    className={leaderboardOption === "most games played" ? "active" : ""}
                    onClick={() => handleLeaderboardToggle("most games played")}
                >
                    Most Games Played
                </button>
                <button
                    className={leaderboardOption === "donk betting board of shame" ? "active" : ""}
                    onClick={() => handleLeaderboardToggle("donk betting board of shame")}
                >
                    Donk Betting Board of Shame
                </button>
                <button
                    className={leaderboardOption === "most aggressive" ? "active" : ""}
                    onClick={() => handleLeaderboardToggle("most aggressive")}
                >
                    Highest VPIPs
                </button>
            </div>
            <div className="leaderboard-table">
              {filteredPlayerList().map((player, index) => (
                <Link
                  key={player.username.toString()}
                  to={player.username.toString()}
                  className="leaderboard-entry"
                >
                  <div className="flex">
                    <div className="item">
                      {player.username}
                    </div>
                    <div className="item">
                      <span>
                        {leaderboardOption === "most aggressive" && `${JSON.parse(player.stats).vpip[0]} / ${JSON.parse(player.stats).vpip[1]}`}
                        {leaderboardOption === "donk betting board of shame" && `${JSON.parse(player.stats).donk[0]} / ${JSON.parse(player.stats).donk[1]}`}
                        {leaderboardOption === "biggest winners" && `${JSON.parse(player.stats).net}`}
                        {leaderboardOption === "most games played" && `${Object.keys(JSON.parse(player.stats).nets).length}`}
                      </span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
            <div className="creators">
                Made by Neil Shah and Brandon Du
            </div>
        </div>
      );
}

export const playerLoader = async () => {
    const res = await fetch('http://devalshah-001-site7.ctempurl.com/api/get')

    if (!res.ok) {
      throw Error('Database is down, please come back another time and let Neil know')
    }

    return res.json()
}