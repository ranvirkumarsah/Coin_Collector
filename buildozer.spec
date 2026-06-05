[app]
title = Coin Collector
package.name = coincollector
package.domain = org.ranvir

source.dir = .
source.include_exts = py,png,json
source.include_patterns = images/*

version = 2.0
orientation = landscape

requirements = python3,pygame,pygame_menu

fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
