# puzzlebot-JuanMa-ws

Workspace ROS 2 Humble para navegación autónoma del **Puzzlebot físico** (Manchester Robotics / Jetson Edition).

Curso **TE3003B — Implementación de robótica inteligente** (Tec de Monterrey), Módulo M3.5: migración de simulación a robot real.

---

## Paquetes

| Paquete | Descripción |
|---|---|
| `puzzlebot_description` | URDF, meshes y configuración de RViz |
| `puzzlebot_gazebo` | Simulación del Puzzlebot en Gazebo |
| `puzzlebot_navigation2` | Nav2 + slam_toolbox (configuración y launches) |
| `puzzlebot_real_robot` | Nodos para el robot físico (corren en la Jetson) |

---

## Requisitos

- Ubuntu 22.04
- ROS 2 Humble
- Paquetes ROS:
  - `ros-humble-navigation2`
  - `ros-humble-nav2-bringup`
  - `ros-humble-slam-toolbox`
  - `ros-humble-rplidar-ros` *(en la Jetson)*
  - `ros-humble-teleop-twist-keyboard`
- `xterm` *(en la laptop)*
- `micro_ros_agent` *(en la Jetson, para comunicación con la Hackerboard)*

---

## Compilar

```bash
cd ~/puzzlebot_JuanMa_ws
colcon build --symlink-install
source install/setup.bash
```

> Si después de hacer `source` sigues teniendo `Package 'puzzlebot_navigation2' not found`, revisa que tu `.bashrc` no esté sourceando otro workspace que sobrescriba este.

---

## Ejecutar Nav2 en el robot físico

Se necesitan dos terminales en máquinas distintas: la **Jetson** del Puzzlebot (vía SSH) y la **laptop**.

### 1. En la Jetson (SSH)

```bash
ros2 launch puzzlebot_real_robot robot.launch.py
```

Levanta:
- `micro_ros_agent` — puente con la Hackerboard
- `sllidar_node` — publica `/scan`
- `robot_state_publisher` — URDF + TFs
- `puzzlebot_localization` — publica `/odom` y TF `odom → base_footprint`
- `puzzlebot_joint_state_publisher` — publica `/joint_states`

### 2. En la laptop

```bash
cd ~/puzzlebot_JuanMa_ws
source install/setup.bash
ros2 launch puzzlebot_navigation2 nav2_real.launch.xml
```

Levanta Nav2 (planner, controller, costmaps, recoveries) y RViz cargando el mapa `map_maze.yaml`.

En RViz:
1. Usa **2D Pose Estimate** para fijar la pose inicial del robot.
2. Usa **Nav2 Goal** para enviar una meta de navegación.

---

## Estructura relevante

```
src/puzzlebot_navigation2/
├── config/
│   ├── nav2_params.yaml        # parámetros afinados para el Puzzlebot
│   └── slam_toolbox.yaml
├── launch/
│   ├── nav2.launch.xml         # Nav2 + Gazebo (simulación)
│   ├── nav2_real.launch.xml    # Nav2 sobre robot físico ← usar este
│   ├── nav2_core.launch.xml    # núcleo Nav2 (lo invocan los wrappers)
│   ├── slam.launch.xml         # SLAM + Gazebo
│   └── slam_core.launch.xml    # SLAM (mapping) + teleop
├── maps/
│   └── map_maze.{pgm,yaml}     # mapa del laberinto
└── rviz/
    ├── nav2.rviz
    └── slam.rviz
```

---

## Autor

**Itzel Hernández** — TE3003B, Tec de Monterrey.
