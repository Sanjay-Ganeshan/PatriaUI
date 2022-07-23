from .lada_dmr import ProjectLadaDMR
from .coalition_pistol import CoalitionPistol
from .basic_ammo import PlasmaChamber, EMChamber, APChamber
from .stat_mod_attachments import TelescopicSight, HolographicSight, Bipod
from .training import BasicTraining, SpecializedTraining

def LuminaDMR() -> ProjectLadaDMR:
    return (
        ProjectLadaDMR()
        .add_attachment(PlasmaChamber())
        .add_attachment(EMChamber())
        .add_attachment(APChamber())
        .add_attachment(TelescopicSight())
        .add_attachment(Bipod())
        .add_attachment(SpecializedTraining())
    )

def LuminaPistol() -> CoalitionPistol:
    return (
        CoalitionPistol()
        .add_attachment(HolographicSight())
        .add_attachment(BasicTraining())
    )
