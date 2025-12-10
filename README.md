# SlicerLayerDisplayableManager

A 3D Slicer module introducing a new displayable manager architecture for layered rendering and interaction handling.

<div style="text-align: center;">
  <img src="https://github.com/KitwareMedical/SlicerLayerDisplayableManager/raw/main/Docs/LayerDisplayableManager.png" style="background-color: white;"/>
</div>

![GitHub stars](https://img.shields.io/github/stars/kitwareMedical/SlicerLayerDisplayableManager)
[![Documentation Status](https://readthedocs.org/projects/slicerlayerdisplayablemanager/badge/?version=latest)](https://slicerlayerdisplayablemanager.readthedocs.io/en/latest/?badge=latest)

## Usage

The [API Reference](https://slicerlayerdisplayablemanager.readthedocs.io/en/latest/index.html)
documentation provides API-level documentation.

## Overview

**SlicerLayerDisplayableManager** is a module designed to simplify the integration of new display
pipelines in 3D Slicer. It introduces a flexible and extensible framework for managing layered rendering, interaction
forwarding, and camera synchronization across multiple pipelines.

This module aims to address common limitations in existing displayable managers by offering a more modular and
injectable design.

## Goals

- Factorize pipeline creation and teardown
- Enable layered rendering and interaction forwarding
- Maintain focus continuity across pipelines
- Synchronize cameras across views and layers
- Centralize render request handling

## Limitations in Current Displayable Managers

The current displayable manager (DM) architecture in 3D Slicer presents several structural and usability limitations:

- Redundant logic: Each DM reimplements pipeline instantiation and renderer setup independently.
- Custom camera sync: Camera synchronization strategies are manually implemented per DM, leading to inconsistent
  behavior.
- Complexity growth: DMs tend to accumulate unrelated logic over time, making them harder to maintain and extend.
- Focus handling: Focus decisions are based on proximity to interaction only, without consideration for layer priority.
- Factory instantiation: DMs are created using string-based factories, preventing injection of shared dependencies or
  services.

## Improvements Introduced by SlicerLayerDisplayableManager

The module introduces a new architecture to improve development quality and scalability for visualization widgets:

- Centralized pipeline management: Pipelines are automatically created and deleted by the displayable manager.
- Dependency injection: Lambda and callback-based creators allow find pipeline creation control and injection of shared
  logic at pipeline creation.
- Modular camera synchronization: A dedicated synchronizer handles camera updates across views and layers for pipelines
  following the main camera.
- Layer-aware interaction: Pipelines declare their render layer with arbitrary values, enabling prioritized focus and
  interaction handling without handling the finer grained VTK logic.
- Python integration: A Python abstract class enables rapid development and integration of pipelines.

These changes simplify the development of new widgets, reduce boilerplate, and improve maintainability of existing
visualization components.

## Key Features

- Pipeline registration via factory and creator API
- Lambda and callback support for dependency injection
- Customizable observer update pattern
- First-class Python abstract pipeline class

For more information on the extension's architecture, please refer to
the [online documentation](https://slicerlayerdisplayablemanager.readthedocs.io/en/latest/extension_architecture.html).

## Installing the extension

The extension can be installed through the extension manager from 3D Slicer 5.10 onwards:

<div style="text-align: center;">
  <img src="https://github.com/KitwareMedical/SlicerLayerDisplayableManager/raw/main/Docs/ExtensionInstall.png" style="background-color: white;"/>
</div>


## Getting Started

To use this extension checkout
the [getting started documentation](https://slicerlayerdisplayablemanager.readthedocs.io/en/latest/getting_started.html).

And refer to
the [examples](https://github.com/KitwareMedical/SlicerLayerDisplayableManager/tree/main/Examples/Python/ModelGlowDM/ModelGlowDM.py).
