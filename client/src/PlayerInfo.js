import { Link, useLoaderData, useParams } from 'react-router-dom';
import React, { useState } from 'react';
import LineGraph from './LineGraph.js';

export default function PlayerInfo() {
  const { username } = useParams();
  const player_info = useLoaderData();
  const nets_history = JSON.parse(player_info[0].stats).nets
  const net_dates = Object.keys(nets_history);
  console.log(net_dates);
  const net_nums = Object.values(nets_history);
  for (let i = 1; i < Object.keys(nets_history).length; i++) {
    net_nums[i] += net_nums[i - 1]
  }
  console.log(net_nums);
  
  const [leaderboardOption, setLeaderboardOption] = useState('games');
  const statistics = JSON.parse(player_info[0].stats);
  const statistics_entries = Object.entries(statistics).filter(
    ([key]) => !['username', 'net', 'raised', 'nets'].includes(key)
  );
  const [currentPage, setCurrentPage] = useState(1);
  const [gamesPerPage] = useState(10);

  const handleLeaderboardToggle = (option) => {
    setLeaderboardOption(option);
    setCurrentPage(1); // Reset to the first page when toggling options
  };

  // Get current games
  const indexOfLastGame = currentPage * gamesPerPage;
  const indexOfFirstGame = indexOfLastGame - gamesPerPage;
  const currentGames = player_info.slice(indexOfFirstGame, indexOfLastGame);

  // Change page
  const paginate = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const game_data = net_nums;
  const labels = []
  for (let i = 1; i <= net_nums.length; i++) {
    labels.push("Game " + i)
  }
  return (
    <div className="playerinfo">
      <div className="leaderboard-table">
        <div className="flex">
          <h3>{username}</h3>
          <div className="item">
            {(JSON.parse(player_info[0].stats).net >= 0 ? '+$' : '-$') +
              Math.abs(JSON.parse(player_info[0].stats).net)}
          </div>
        </div>
      </div>

      <LineGraph  data={game_data} labels={labels}/>

      <div className="board">
        <div className="duration">
          <button
            className={leaderboardOption === 'games' ? 'active' : ''}
            onClick={() => handleLeaderboardToggle('games')}
          >
            Games
          </button>
          <button
            className={leaderboardOption === 'stats' ? 'active' : ''}
            onClick={() => handleLeaderboardToggle('stats')}
          >
            Stats
          </button>
        </div>
      </div>

      {leaderboardOption === 'games' && (
        <div>
          <div className="leaderboard-table">
            {currentGames.map((game) => (
              <Link to={`/game/${game.id}`} key={game.id} className="leaderboard-entry">
                <div className="flex">
                  <div className="item">{game.name.replace('logs/', '')}</div>
                  <div className="item">{new Date(game.date).toLocaleDateString()}</div>
                </div>
              </Link>
            ))}
          </div>

          <div className="pagination">
            {player_info.length > gamesPerPage && (
              <ul>
                {Array(Math.ceil(player_info.length / gamesPerPage))
                  .fill()
                  .map((_, index) => (
                    <li
                      key={index}
                      className={currentPage === index + 1 ? 'active' : ''}
                      onClick={() => paginate(index + 1)}
                    >
                      {index + 1}
                    </li>
                  ))}
              </ul>
            )}
          </div>
        </div>
      )}

      {leaderboardOption === 'stats' && (
        <table className="stats-table">
          <tbody>
            {statistics_entries.map(([name, data]) => (
              <tr key={name}>
                <td>{name}</td>
                <td>{data[0]} / {data[1]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}


export const playerInfoLoader = async ({ params }) => {
    const { username } = params
    const res = await fetch('http://localhost:3001/api/get/' + username)

    
    return res.json()
}