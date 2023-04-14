import React, { useState, useEffect } from "react";
import "./App.css";
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import {Stage, Layer, Rect, Text, Circle} from "react-konva";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem'
import {Button} from "@mui/material";
import Slider from '@mui/material/Slider';
import {TransformWrapper, TransformComponent} from "react-zoom-pan-pinch";

const various_colors = ["blue", "red", "green", "purple", "gray", "darkgreen", "black"]
let gridworld_array = [];

const create_gridworld_two = (arr, lookup, square_size) => {
        const x_len = arr.length;
        const y_len = arr[0].length;
        gridworld_array = Array(x_len * y_len);
        let counter = 0;
        for (let i = 0; i < x_len; i++) {
            for (let j = 0; j < y_len; j++) {
                gridworld_array[counter] = <Rect
                        perfectDrawEnabled={false}
                        listening={false}
                        shadowForStrokeEnabled={false}
                        hitStrokeWidth={0}
                        x={i * square_size}
                        y={j * square_size}
                        width={square_size}
                        height={square_size}
                        fill = {lookup[arr[i][j]]}/>
                counter += 1
            }
        }
    }

const get_agent_tab = (info_size) => {
    return <div
                    hidden = {this.state.tab_value !== 0}
                    >
            {"selected agent: "}
                        <Select
                        value = {this.state.selected_agent}
                        label = "Agent"
                        onChange={(event) => this.setState({
                            selected_agent:  event.target.value}
                            )}
                        >
                            {
                                Object.keys(this.state.agent_names).map((key, value) => {
                                        return <MenuItem value={key} color = {various_colors[value]}>{this.state.agent_names[key]}</MenuItem>
                                    })
                            }
                        </Select>
                        {

                            this.display_inventory(this.state.agent_data[this.state.selected_agent])
                        }
                            <LineChart
                              width={window.innerWidth * info_size}
                              height={window.innerHeight * 0.4}
                              data={this.state.agent_data[this.state.selected_agent]}
                              margin={{
                                top: 5,
                                left: 0,
                              }}
                            >
                              <XAxis dataKey="idx" label = "timestep" />
                              <YAxis label = "quantity"/>
                              <Tooltip />
                              <Legend />
                              <Line type="monotone" dataKey="ore" stroke="red" activeDot={{ r: 8 }} />
                              <Line type="monotone" dataKey="metals" stroke="black" />
                                <Line type="monotone" dataKey="coal" />
                                <Line type="monotone" dataKey="wood" stroke="green" />
                            </LineChart>
                                        <LineChart
                              width={window.innerWidth * info_size}
                              height={window.innerHeight * 0.4}
                              data={this.state.agent_totals}
                              margin={{
                                top: 5,
                                left: 0,
                              }}
                            >
                              <XAxis dataKey="idx" label = "timestep" />
                              <YAxis label = "quantity"/>
                              <Tooltip />
                              <Legend />
                                {
                                Object.keys(this.state.agent_names).map((key, value) => {
                                        return <Line  type="monotone" dataKey= {this.state.agent_names[key]} stroke = {various_colors[value]}/>
                                    })
                            }
                            </LineChart>
                    </div>
}


export default class App extends React.PureComponent {
    state = {
        squareSize: 128,
        gridworld_color_lookup: {
            0: "#e3b94d",
            1: "red",
            2: "green",
            3: "black",
            4: "yellow",
        },
        frontend_ready: false,
        agent_names: {0: "NoAgent"},
        gridworld: [[0]],
        gridworld_x: 0,
        gridworld_y: 0,
        agent_locations: [[0, 0]],
        agent_data: [[{"nothing": 0}], [{"nothing": 0}]],
        agent_totals: {},
        tab_value: 0,
        selected_agent: 0
    }

    render_agents = (agent_locations) => {
        return agent_locations.map((value, index) =>
            <Circle
                    x={value[0] * this.state.squareSize + (this.state.squareSize / 2)}
                    y={value[1] * this.state.squareSize+ (this.state.squareSize / 2)}
                    width={this.state.squareSize}
                    height={this.state.squareSize}
                    fill={various_colors[index]}
        >
        </Circle>)
    }


    create_gameboard = (board, lookup) => {
        create_gridworld_two(board, lookup, this.state.squareSize)
        return <Stage
            width={(this.state.squareSize + 0.25) * this.state.gridworld_x}
            height={(this.state.squareSize + 0.25) * this.state.gridworld_y}
            perfectDrawEnabled={false}
            listening={false}
            shadowForStrokeEnabled={false}
            hitStrokeWidth={0}
            >
            <Layer
                perfectDrawEnabled={false}
                listening={false}
                shadowForStrokeEnabled={false}
                hitStrokeWidth={0}
            >
                {gridworld_array}
                {this.render_agents(this.state.agent_locations)}
            </Layer>
    </Stage>
    }

    componentDidMount() {
        this.interval = setInterval(() =>
        fetch("http://127.0.0.1:5000/data")
                    .then((response) => response.json())
                    .then((data) => {
                        this.setState({...data})
                    }),
            2
        )
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    display_inventory(inventory) {

        let len = inventory.length;
        let current_inventory = inventory[len - 1];
        console.log(current_inventory)
        return <div>
            {"Current Inventory: "}
            {
                Object.keys(current_inventory).map((key, value) => {
                    return <div>{key}{" "}{current_inventory[key]}</div>
                })
            }
            </div>

    }

    get_agent_tab(info_size){
        return  <div
                    hidden = {this.state.tab_value !== 0}
                    >
            {"selected agent: "}
                        <Select
                        value = {this.state.selected_agent}
                        label = "Agent"
                        onChange={(event) => this.setState({
                            selected_agent:  event.target.value}
                            )}
                        >
                            {
                                Object.keys(this.state.agent_names).map((key, value) => {
                                        return <MenuItem value={key} color = {various_colors[value]}>{this.state.agent_names[key]}</MenuItem>
                                    })
                            }
                        </Select>
                        {

                            this.display_inventory(this.state.agent_data[this.state.selected_agent])
                        }
                            <LineChart
                              width={window.innerWidth * info_size}
                              height={window.innerHeight * 0.4}
                              data={this.state.agent_data[this.state.selected_agent]}
                              margin={{
                                top: 5,
                                left: 0,
                              }}
                            >
                              <XAxis dataKey="idx" label = "timestep" />
                              <YAxis label = "quantity"/>
                              <Tooltip />
                              <Legend />
                              <Line type="monotone" dataKey="ore" stroke="red" activeDot={{ r: 8 }} />
                              <Line type="monotone" dataKey="metals" stroke="black" />
                                <Line type="monotone" dataKey="coal" />
                                <Line type="monotone" dataKey="wood" stroke="green" />
                            </LineChart>
                                        <LineChart
                              width={window.innerWidth * info_size}
                              height={window.innerHeight * 0.4}
                              data={this.state.agent_totals}
                              margin={{
                                top: 5,
                                left: 0,
                              }}
                            >
                              <XAxis dataKey="idx" label = "timestep" />
                              <YAxis label = "quantity"/>
                              <Tooltip />
                              <Legend />
                                {
                                Object.keys(this.state.agent_names).map((key, value) => {
                                        return <Line  type="monotone" dataKey= {this.state.agent_names[key]} stroke = {various_colors[value]}/>
                                    })
                            }
                            </LineChart>
                    </div>
    }


    async initialize_frontend() {
        this.setState({frontend_ready: true})
        await fetch("/frontend_ready", {
            method: "POST",
            mode: "cors",
            body: {
                frontend_ready: true
            }
        })
    }


    render() {
        let info_size = 0.4;
        let control_panel_size = 0.1;
        let gridworld_width = window.innerWidth * (1 - info_size);
        let gridworld_height = window.innerHeight *  (1 - control_panel_size)
        let grid = this.create_gameboard(this.state.gridworld, this.state.gridworld_color_lookup)

        if (this.state.gridworld_y !== 0 && !this.state.frontend_ready) {
            this.initialize_frontend()
        }

        return (<div style={
            {
                width: window.innerWidth,
                height: window.innerHeight,
                backgroundColor: "black"
            }}>
            <TransformWrapper>

                    <TransformComponent>
            <div style = {{
                width: gridworld_width,
                height: gridworld_height,
                backgroundColor: "gray",
            }}>
                {grid}
            </div></TransformComponent>

                </TransformWrapper>
            <div style={
            {
                position: "absolute",
                top: 0,
                left: gridworld_width,
                width: window.innerWidth - gridworld_width,
                height: window.innerHeight,
                backgroundColor: "black"
            }}
            >
                <Box sx = {{width: '100%', height: '100%', backgroundColor: 'white'}}>
                    <Tabs value = {this.state.tab_value} onChange={(event, value) => this.setState({tab_value: value})}>
                        <Tab label = "Agents" value={0}>{}</Tab>
                        <Tab label = "Marketplace" value={1}>
                            {"hello"}
                        </Tab>
                        <Tab label = "Markets" value={2}>
                            {"hello"}
                        </Tab>
                    </Tabs>
                    {this.get_agent_tab(info_size)}

                </Box>
            </div>
                        <div style={
            {
                position: "absolute",
                top: window.innerHeight *  (1 - control_panel_size),
                left: 0,
                width: gridworld_width,
                height: window.innerHeight * control_panel_size,
                backgroundColor: "white"
            }}
            >
        <Box
            width={"100%"}
        >
            {"Environment squareSize"} {this.state.squareSize}
            <Button
                                variant={"contained"}
                                backgroundColor={"green"}
            aria-label={"increase square size"}
            onClick={() => this.setState({squareSize: this.state.squareSize + 1})}
            >
                {"+"}
            </Button>
            <Button
                variant={"contained"}
                backgroundColor = {"red"}
                aria-label={"increase square size"}
                onClick={() => this.setState({squareSize: this.state.squareSize - 1})}
            >
                {"-"}
            </Button>
        </Box>
                            {this.state.frontend_ready ? "true": "false"}
            </div>
        </div>)
    }
}



