from http import HTTPStatus
from flask import Blueprint, jsonify, request

from app.api.model.bag import Bag
from app.api.model.cuboid import Cuboid
from app.api.schema.cuboid import CuboidSchema
from app.api.db import db

cuboid_api = Blueprint("cuboid_api", __name__)


@cuboid_api.route("/", methods=["GET"])
def list_cuboids():
    cuboid_ids = request.args.getlist("cuboid_id")
    cuboid_schema = CuboidSchema(many=True)
    cuboids = Cuboid.query.filter(Cuboid.id.in_(cuboid_ids)).all()

    return jsonify(cuboid_schema.dump(cuboids)), HTTPStatus.OK


@cuboid_api.route("/<int:cuboid_id>", methods=["GET"])
def get_cuboid(cuboid_id):
    cuboid_schema = CuboidSchema()
    cuboid = Cuboid.query.get(cuboid_id)

    if cuboid:
        return jsonify(cuboid_schema.dump(cuboid)), HTTPStatus.OK
    return jsonify(message="Cuboid not found"), HTTPStatus.NOT_FOUND


@cuboid_api.route("/", methods=["POST"])
def create_cuboid():
    content = request.json

    cuboid_schema = CuboidSchema()
    cuboid = Cuboid(
        width=content["width"],
        height=content["height"],
        depth=content["depth"],
        bag_id=content["bag_id"],
    )

    bag = Bag.query.get(content["bag_id"])

    if bag:
        cuboid = cuboid.create_cuboid(bag.available_volume)
        if cuboid:
            return jsonify(cuboid_schema.dump(cuboid)), HTTPStatus.CREATED
        message = "Insufficient capacity in bag"
        return jsonify(message=message), HTTPStatus.UNPROCESSABLE_ENTITY
    cuboid.message = f"Bag id {content['bag_id']} not found"
    return jsonify(cuboid_schema.dump(cuboid)), HTTPStatus.NOT_FOUND


@cuboid_api.route('/<int:cuboid_id>/update', methods=['PATCH'])
def update_cuboid(cuboid_id):
    cuboid_schema = CuboidSchema()
    content = request.json

    cuboid = Cuboid.query.get(cuboid_id)
    if cuboid:
        bag = Bag.query.get(cuboid.bag_id)
        new_cuboid_volume = content["width"] * content["depth"] * content["height"]
        new_bag_available_volume = bag.available_volume + cuboid.volume

        if new_cuboid_volume <= new_bag_available_volume:
            cuboid.update_cuboid(width=content["width"],
                                 depth=content["depth"],
                                 height=content["height"])
            return jsonify(cuboid_schema.dump(cuboid)), HTTPStatus.OK

        message = "Insufficient capacity in bag"
        return jsonify(message=message), HTTPStatus.UNPROCESSABLE_ENTITY

    message = "Cuboid not found"
    return jsonify(message=message), HTTPStatus.NOT_FOUND


@cuboid_api.route('<int:cuboid_id>/delete', methods=["DELETE"])
def delete_cuboid(cuboid_id):
    cuboid = Cuboid.query.get(cuboid_id)
    if cuboid:
        db.session.delete(cuboid)
        db.session.commit()
        message = "Cuboid deleted"
        return jsonify(message=message), HTTPStatus.OK

    message = "Cuboid not found"
    return jsonify(message=message), HTTPStatus.NOT_FOUND
