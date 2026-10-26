<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     * Tabel inventories — stok produk per gudang
     */
    public function up(): void
    {
        Schema::create('inventories', function (Blueprint $table) {
            $table->id();
            $table->foreignId('warehouse_id')
                  ->constrained('warehouses')
                  ->cascadeOnDelete()
                  ->comment('Relasi ke tabel warehouses');
            $table->foreignId('product_id')
                  ->constrained('products')
                  ->cascadeOnDelete()
                  ->comment('Relasi ke tabel products');
            $table->integer('quantity_on_hand')->default(0)->comment('Jumlah stok fisik saat ini');
            $table->integer('quantity_reserved')->default(0)->comment('Jumlah stok yang sudah dipesan / direservasi');
            $table->integer('reorder_point')->default(0)->comment('Titik reorder — stok minimum sebelum pembelian ulang');
            $table->date('last_counted_date')->nullable()->comment('Tanggal stock opname terakhir');
            $table->timestamps();

            // Satu produk hanya satu record per gudang
            $table->unique(['warehouse_id', 'product_id']);

            // Index untuk query stok
            $table->index('product_id');
            $table->index('warehouse_id');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('inventories');
    }
};
