import React from 'react'
import "./home.css"
import { Chart, ArcElement, Tooltip, Legend, CategoryScale, registerables } from "chart.js";
import { Doughnut, Line } from "react-chartjs-2";

Chart.register(...registerables);

export default function Home() {

    let chartData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: 'Network Performance',
            data: [80, 70, 90, 75, 85, 80],
            // fill: false,
            // borderColor: 'rgb(75, 192, 192)',
            // tension: 0.4
        }]
    }

    var chartOptions = {
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                ticks: {
                    stepSize: 20
                }
            }
        }
    };

    var chartOptions = {
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                ticks: {
                    stepSize: 20
                }
            }
        }
    };

    // Create the line chart
    // var resourceChart = new Chart(chartCanvas, {
    //     type: 'line',
    //     data: chartData,
    //     options: chartOptions
    // });

    var chartData1 = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: 'Resource Usage',
            data: [50, 60, 40, 70, 50, 80],
            fill: false,
            borderColor: 'rgb(154, 205, 50)',
            tension: 0.4
        }]
    };

    // Create the line chart
    // var networkChart1 = new Chart(chartCanvas, {
    //     type: 'line',
    //     data: chartData,
    //     options: chartOptions
    // });


  return (
    <div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <header>
        <div class="search-bar">
            <input type="text" class="search-input" placeholder="Search"/>
            <button class="search-button">Find</button>
        </div>
    </header>
    
    <div class="sidenav">
                
        <a href="#" class="brand">
            Atomic<span class="green">Team</span>
        </a>
        <br/>
        <a href="transaction.php">Transactions</a>
        <a href="blocks.php">Blocks</a>
        <a href="accounts.php">Accounts</a>
        <a href="suppliers.php">Suppliers</a>
    </div>
    <h1>Monitoring and Tracking Tool</h1>
    <center>
    <table class="table">
  <tr>
    <th>Latest Block</th>
    <th>Average Block Time</th>
    <th>Total Transactions</th>
    <th>Total Addresses</th>
    
  </tr>
  <tr>
    <th>70782</th>
    <td>2.6s</td>
    <td>40,429</td>
    <td>1,597</td>
  </tr>
  
</table>
</center>
    <main>
        <section>
            <h2>Network Performance</h2>
            <canvas id="networkChart"></canvas>
            <Line data={chartData}></Line>
        </section>

    
    



        
        <section>
            <h2>Resource Usage</h2>
            <canvas id="resource-chart"></canvas>
            <Line data={chartData1}></Line>
        </section>
        
        <section>
            <h2>Storage Provider Node Status</h2>
            <ul class="status-list">
                <li class="status-item">
                    <span class="status-label">Node 1:</span>
                    <span class="status-value">Online</span>
                </li>
                <li class="status-item">
                    <span class="status-label">Node 2:</span>
                    <span class="status-value">Offline</span>
                </li>
                <li class="status-item">
                    <span class="status-label">Node 3:</span>
                    <span class="status-value">Online</span>
                </li>
            </ul>
        </section>
        
        <section>
            <h2>Potential Issues</h2>
            <div class="notification">
        <div class="icon"></div>
        <div class="content">
            <h3>Important Notification</h3>
            <p>There is a potential issue with the storage provider. Please take immediate action to resolve it.</p>
        </div>
    </div>
        </section>
    </main>
    
    <footer>
        <p>AtomicTeam 2023</p>
    </footer>
</div>
  )
}
