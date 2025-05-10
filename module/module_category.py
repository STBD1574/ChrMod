# -*- coding: utf-8 -*-

class ModuleCategory(tuple):
    @property
    def name(self):
        return self[0]

    @property
    def icon(self):
        return self[1]

class ModuleCategories(object):
    COMBAT = ModuleCategory("Combat", "icon_combat.png")
    MOVEMENT = ModuleCategory("Movement", "icon_movement.png")
    VISUAL = ModuleCategory("Visual", "icon_visual.png")
    MISC = ModuleCategory("Misc", "icon_misc.png")